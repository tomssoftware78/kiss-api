import re
import time

import uvicorn
import json
import os
from uuid import UUID

import iris

from datetime import datetime, timedelta, date
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated
from contextlib import asynccontextmanager
from kissutils import database_instance

from dotenv import load_dotenv
load_dotenv()
fake_users_db = json.loads(os.environ.get('USERS'))


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

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_instance.connect()
    yield

app = FastAPI(lifespan=lifespan)
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
    id: int
    name: str
    last_notice: Union[str, None]
    last_magistrat: Union[str, None]
    last_enqueteur: Union[str, None]
    last_email: Union[str, None]
    last_service: Union[str, None]

    @classmethod
    def custom_init(cls, id: int, name: str, last_notice: str, last_magistrat: str,
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
    sin: Union[str, None]
    mark_model_str: Union[str, None]
    type: Union[str, None]
    operator_identity: Union[str, None]
    pv_number: Union[str, None]
    urgent: bool
    date_in: date
    date_end: date
    date_out: date

    @classmethod
    def custom_init(cls, id: int, number: str, sin: str, mark_model_str: str, type: str, operator_identity: str,
                    pv_number: str, urgent: bool, date_in: date, date_end: date, date_out: date):

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


@app.get("/case/{case_id}", response_model=KissCase)
def get_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    term = ((str)(case_id))
    term = term[0:2]+"/" + term[2:]
    return search_kiss_case(current_user, term, badge_id)[0]

def convertKissDetailToCaseID(detail):
    return (int)(re.sub(r'[^0-9]', '', detail)[:-3])

def convertKissDetailToCaseName(detail):
    return detail.removeprefix("RCCU/")[:-4]

def convertCaseIDToKissDetail(id):
    caseId = ((str)(id))
    caseId = "RCCU/" + caseId[0:2]+"/" + caseId[2:6] + "/"
    return caseId

@app.post("/case/search", response_model=list[KissCase])
def search_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], term: str, badge_id: int):
    cases = []
    term4chars = term.rjust(4, "0")
    print(term4chars)

    query = "SELECT TOP 10 c.IdDetail AS id, c.idRelatie->idgebeurtenis->idDocument->iddossier->Naam AS CaseName, " \
        "c.idRelatie->idgebeurtenis->idDocument->iddossier->notitienummer AS last_notice, " \
        "c.idRelatie->idgebeurtenis->idDocument->iddossier->idMagistraat->Naam AS last_magistrat, " \
        "{fn CONCAT({fn CONCAT(g.Voornaam, ' ')}, g.naam)} AS last_enqueteur, g.paswoord AS last_email, " \
        "c.idRelatie->idgebeurtenis->idDocument->iddossier->idEenheid->Naam AS last_service " \
        "FROM KISS.tblCCUdetail c LEFT JOIN Kiss.tblgebruikers g ON c.nagezienDoor = g.Stamnummer " \
        "WHERE c.DatumOUT <> \"1900-01-01\" "

    termcondition = "c.IdDetail like 'RCCU/%" + term4chars + "/0%'"

    if not term.isdigit():
        # also check names of cases
        termcondition = termcondition + " OR c.idRelatie->idgebeurtenis->idDocument->iddossier->Naam like '%" + str(term) + "%'"

    query = query + " AND (" + termcondition + ")"

    if check_limited_to_team(badge_id):
        teamId = str(get_team(badge_id))
        query = query + " AND c.idRelatie->idgebeurtenis->idDocument->iddossier->idTeam = " + teamId

    query = query + " ORDER BY id DESC"
    result = database_instance.fetch_rows(query)

    ids_processed = []

    for row in result:
        print(str(row))
        caseId = convertKissDetailToCaseID(row[0])
        if caseId not in ids_processed:
            name = row[1]
            if name == "DOMEIN RCCU":
                name = convertKissDetailToCaseName(row[0])
            cases.append(KissCase.custom_init(caseId, name, row[2], row[3], row[4], str(row[5]), row[6]))
            ids_processed.append(caseId)

    return cases

def convert_date_string(d):
    if d is not None and len(d) >=10:
        return d[0:4] + '-' + d[5:7] + '-' + d[8:10]

    return d

@app.get("/items/{case_id}", response_model=list[KissItem])
def get_kiss_items_from_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    items = []

    query = "SELECT c.ID as id, c.IdDetail AS Number, c.reserv1 AS sin, c.merk->beschrijving AS mark_model_str, " \
            "c.type AS type, {fn CONCAT({fn CONCAT(g.Voornaam, ' ')}, g.naam)} AS operator_identity, " \
            "c.idRelatie->idgebeurtenis->idDocument->Docnr AS pv_number, c.prioriteit AS urgent, " \
            "CONVERT(VARCHAR(20),c.DatumIn, 111) AS Date_in, CONVERT(VARCHAR(20),c.DatumIBN, 111) AS Date_end, CONVERT(VARCHAR(20),c.DatumOut, 111) AS Date_out, " \
            " c.opdracht->beschrijving AS opdracht " \
            "FROM KISS.tblCCUdetail c LEFT JOIN Kiss.tblgebruikers g ON c.nagezienDoor = g.Stamnummer " \
            "WHERE c.DatumOUT <> \"1900-01-01\" AND c.IdDetail like '" + convertCaseIDToKissDetail(case_id) + "%' "

    if check_limited_to_team(badge_id):
        teamId = str(get_team(badge_id))
        query = query + " AND c.idRelatie->idgebeurtenis->idDocument->iddossier->idTeam = " + teamId

    query = query + " ORDER BY id DESC"
    result = database_instance.fetch_rows(query)

    for row in result:
        print(str(row))
        items.append(KissItem.custom_init(row[0], row[1], row[2], str(row[4]) + ' ' + str(row[3]), row[11], row[5],
                                          row[6], False, convert_date_string(row[8]), convert_date_string(row[9]),
                                          convert_date_string(row[10])))

    return items

@app.post("/items", response_model=list[KissItem])
def get_kiss_items(current_user: Annotated[User, Depends(get_current_active_user)], item_ids: list[int], badge_id: int):
    items = []

    string_list = ",".join(str(num) for num in item_ids)

    query = "SELECT c.ID as id, c.IdDetail AS Number, c.reserv1 AS sin, c.merk->beschrijving AS mark_model_str, " \
            "c.type AS type, {fn CONCAT({fn CONCAT(g.Voornaam, ' ')}, g.naam)} AS operator_identity, " \
            "c.idRelatie->idgebeurtenis->idDocument->Docnr AS pv_number, c.prioriteit AS urgent, " \
            "CONVERT(VARCHAR(20),c.DatumIn, 111) AS Date_in, CONVERT(VARCHAR(20),c.DatumIBN, 111) AS Date_end, CONVERT(VARCHAR(20),c.DatumOut, 111) AS Date_out " \
            "FROM KISS.tblCCUdetail c LEFT JOIN Kiss.tblgebruikers g ON c.nagezienDoor = g.Stamnummer " \
            "WHERE c.DatumOUT <> \"1900-01-01\" AND c.ID in (" + string_list + ") "

    if check_limited_to_team(badge_id):
        teamId = str(get_team(badge_id))
        query = query + " AND c.idRelatie->idgebeurtenis->idDocument->iddossier->idTeam = " + teamId

    query = query + " ORDER BY id DESC"
    result = database_instance.fetch_rows(query)

    for row in result:
        print(str(row))
        items.append(KissItem.custom_init(row[0], row[1], row[2], row[3], row[4], row[5],
                                          row[6], False, convert_date_string(row[8]), convert_date_string(row[9]),
                                          convert_date_string(row[10])))

    return items

def retrier(counter, func, args):
    try:
        return func(*args)
    except Exception as e:
        print("Retrier: " + str(counter) + " " + str(e))
        if counter > 0:
            time.sleep(1)
            return retrier(counter-1, func, args)
        else:
            raise e

def connect_to_iris(localport):
    connection_string = "127.0.0.1:" + str(localport) + "/" + connection_kiss_schema
    return iris.connect(connection_string, username=connection_kiss_username, password=connection_kiss_password)

def check_limited_to_team(badge_id):
    result = database_instance.fetch_rows(
        "SELECT  min(tdn.Toelating) AS Toelating FROM KISS.tblGebruikersProfielen g "
        "LEFT JOIN KISS.tblToegangsDomeinen tdn ON (g.idProfiel = tdn.IdProfiel) "
        "LEFT JOIN KISS.tblToegangDomein td ON (td.IdToegangsDomein= tdn.IdToegangsDomein) "
        "WHERE tdn.IdToegangsDomein = 2 AND g.IdStamnummer = " + str(badge_id))

    for row in result:
        return row[0] == 3

    return True


def get_team(badge_id):
    result = database_instance.fetch_rows(
        "SELECT g.idTeam FROM kiss.tblGebruikers g WHERE Stamnummer = " + str(badge_id))

    for row in result:
        return row[0]

    return ""

@app.get("/user/{badge_id}", response_model=KissUser)
async def get_kiss_user(current_user: Annotated[User, Depends(get_current_active_user)], badge_id: int):
    result = database_instance.fetch_rows("SELECT g.Stamnummer AS badgeid, g.Naam AS lastname, g.Voornaam AS firstname, "
                           "g.Paswoord AS email, e.naam AS unit, g.idTeam->beschrijving AS division FROM kiss.tblGebruikers g LEFT JOIN kiss.piceenheden e ON (g.IdEenheid = e.id) WHERE Stamnummer = " + str(badge_id))

    for row in result:
        print(str(row))
        unit = row[5]
        superuser = (unit == 'RCCU')
        uuid = str(UUID('00000000000000000000000' + str(badge_id)))
        return KissUser.custom_init(uuid, str(row[0]), row[2], row[1], row[3], unit, row[4], superuser, superuser,
                                    superuser, "NL", None, None)

    raise HTTPException(status_code=404, detail="User " + str(badge_id) + " not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)