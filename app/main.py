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

from service.kiss_search_service import KissSearchService
from service.gebruikers_service import GebruikersService
from security.security_service import SecurityService
from security.model.security_model import TokenData, Token, User
from dao.kiss.search.kiss_search_dao import KissSearchDao
from model import Item, KissCase, KissUser, KissItem
from cicd.rest.response_chain.response_chain_factory import VersionResponseChainFactory

import logging.config
import yaml

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'logging_config.yml')

with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

#from routes.i2_connector_routes import router as i2_connector_router

load_dotenv()
fake_users_db = json.loads(os.environ.get('USERS'))


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30





@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_instance.connect()
    yield

app = FastAPI(lifespan=lifespan)
app.ssh_connection = None
app.ssh_forward_ctx = None
#app.include_router(i2_connector_router)

security_service = SecurityService(SECRET_KEY, ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(security_service.get_oauth2_scheme())]):
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
    user = security_service.get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = security_service.authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def clear_connection():
    app.ssh_connection = None
    app.ssh_forward_ctx = None


@app.get("/case/{case_id}", response_model=KissCase)
def get_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    term = ((str)(case_id))
    term = term[0:2]+"/" + term[2:]
    return search_kiss_case(current_user, term, badge_id)[0]

@app.post("/case/search", response_model=list[KissCase])
def search_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], term: str, badge_id: int):
    cases = []
    
    kiss_search_service = KissSearchService()
    cases = kiss_search_service.search_kiss_case(term=term, badge_id=badge_id)

    return cases

@app.get("/items/{case_id}", response_model=list[KissItem])
def get_kiss_items_from_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    items = []

    kiss_search_service = KissSearchService()
    items = kiss_search_service.get_kiss_items_from_case(case_id=case_id, badge_id=badge_id)

    return items
    

@app.post("/items", response_model=list[KissItem])
def get_kiss_items(current_user: Annotated[User, Depends(get_current_active_user)], item_ids: list[int], badge_id: int):
    items = []

    kiss_search_service = KissSearchService()
    items = kiss_search_service.items(item_ids=item_ids, badge_id=badge_id)

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

@app.get("/user/{badge_id}", response_model=KissUser)
async def get_kiss_user(current_user: Annotated[User, Depends(get_current_active_user)], badge_id: int):
    
    gebruikers_service = GebruikersService()

    user = gebruikers_service.get_user(badge_id=badge_id)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User " + str(badge_id) + " not found")

# Define the version endpoint
@app.get("/version")
async def get_version():
    version_response_chain = VersionResponseChainFactory().create_version_response_chain()
    version_response = version_response_chain.create_version_response()
    json_response = version_response.model_dump_json()
    logger.info("Version response: %s", json_response)

    return json_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)