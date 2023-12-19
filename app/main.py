import time

import uvicorn
import json
import os
from uuid import UUID

import iris
from fabric import Connection
from unidecode import unidecode

from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from dotenv import load_dotenv
load_dotenv()
connection_ssh_jump = os.environ.get('CONNECTION_SSH_JUMP')
fake_users_db = json.loads(os.environ.get('USERS'))

connection_local_port = int(os.environ.get('LOCAL_PORT'))
connection_kiss_port = int(os.environ.get('KISS_IRIS_PORT'))
connection_kiss_ip = os.environ.get('KISS_IRIS_IP')
connection_kiss_username = os.environ.get('KISS_USERNAME')
connection_kiss_password = os.environ.get('KISS_PASSWORD')
connection_kiss_schema = os.environ.get('KISS_SCHEMA')



# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.ssh_connection = None
app.ssh_forward_ctx = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

class Item(BaseModel):
    name: str

    @classmethod
    def custom_init(cls, name: str):
        return cls(name=name)

class KissCase(BaseModel):
    id: str
    name: str
    last_notice: str
    last_magistrat: str
    last_enqueteur: str
    last_email: str
    last_service: str

    @classmethod
    def custom_init(cls, id: str, name: str, last_notice: str, last_magistrat: str,
                    last_enqueteur: str, last_email: str, last_service: str):
        return cls(id=id,
               name=name,
               last_notice=last_notice,
               last_magistrat=last_magistrat,
               last_enqueteur=last_enqueteur,
               last_email=last_email,
               last_service=last_service)

class KissUser(BaseModel):
    uuid: str
    badgeid: str
    firstName: str
    lastName: str
    email: str
    unit: str
    division: str
    operator: bool
    staff: bool
    superuser: bool
    language: str
    mobilePhone: Union[str, None]
    officePhone: Union[str, None]

    @classmethod
    def custom_init(cls, uuid: str, badgeid: str, firstName: str, lastName: str,
                    email: str, unit: str, division: str, operator: bool, staff: bool,
                    superuser: bool, language: str, mobilePhone: str, officePhone: str):
        return cls(uuid=uuid,
                   badgeid=badgeid,
                   firstName=firstName,
                   lastName=lastName,
                   email=email,
                   unit=unit,
                   division=division,
                   operator=operator,
                   staff=staff,
                   superuser=superuser,
                   language=language,
                   mobilePhone=mobilePhone,
                   officePhone=officePhone)

class KissItem(BaseModel):
    id: int
    number: str
    sin: str
    mark_model_str: str
    type: str
    operator_identity: str
    pv_number: str
    urgent: bool
    date_in: datetime
    date_end: datetime
    date_out: datetime

    @classmethod
    def custom_init(cls, id: int, number: str, sin: str, mark_model_str: str, type: str, operator_identity: str,
                    pv_number: str, urgent: bool, date_in: datetime, date_end: datetime, date_out: datetime):

        return cls(id=id,
                   number=number,
                   sin=sin,
                   mark_model_str=mark_model_str,
                   type=type,
                   operator_identity=operator_identity,
                   pv_number=pv_number,
                   urgent=urgent,
                   date_in=date_in,
                   date_end=date_end,
                   date_out=date_out)

def clear_connection():
    app.ssh_connection = None
    app.ssh_forward_ctx = None


def ensure_connection():
    if app.ssh_connection == None or not app.ssh_connection.is_connected:
        app.ssh_connection = Connection(connection_ssh_jump)
        app.ssh_forward_ctx = app.ssh_connection.forward_local(local_port=connection_local_port, remote_port=connection_kiss_port, remote_host=connection_kiss_ip, local_host="127.0.0.1")
        app.ssh_forward_ctx.__enter__()
        print("after creation")
        time.sleep(1)

@app.get("/case/{case_id}", response_model=KissCase)
def get_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    print("TODO")
    raise HTTPException(status_code=404, detail="case " + str(case_id) + " not found for " + str(badge_id))

@app.get("/case/search/{term}", response_model=list[KissCase])
def search_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], term: str, badge_id: int):
    print("TODO")
    return []

@app.get("/items/{case_id}", response_model=list[KissItem])
def search_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    print("TODO")
    return []

@app.get("/items", response_model=list[KissItem])
def search_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], item_ids: list[int], badge_id: int):
    print("TODO")
    return []

@app.get("/user/{badge_id}", response_model=KissUser)
def get_kiss_user(current_user: Annotated[User, Depends(get_current_active_user)], badge_id: int):
    ensure_connection()
    connection_string = "127.0.0.1:" + str(connection_local_port) + "/" + connection_kiss_schema
    try:
        connection = iris.connect(connection_string, username=connection_kiss_username, password=connection_kiss_password)
        print("connected")
        cursor = connection.cursor()
        cursor.execute("SELECT g.Stamnummer AS badgeid, g.Naam AS lastname, g.Voornaam AS firstname, "
                       "g.Paswoord AS email, e.naam AS unit, g.idTeam->beschrijving AS division FROM kiss.tblGebruikers g LEFT JOIN kiss.piceenheden e ON (g.IdEenheid = e.id) WHERE Stamnummer = " + str(badge_id))

        for row in cursor.fetchall():
            print(str(row))
            unit = row[5]
            superuser = (unit == 'RCCU')
            uuid = str(UUID('00000000000000000000000' + str(badge_id)))
            return KissUser.custom_init(uuid, str(row[0]), row[2], row[1], row[3], unit, row[4], superuser, superuser, superuser, "NL", None, None)

    except Exception as e:
        print(str(e))
        clear_connection()
        raise e

    raise HTTPException(status_code=404, detail="User " + str(badge_id) + " not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)