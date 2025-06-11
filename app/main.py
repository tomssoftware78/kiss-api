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
from model import Item, KissCase, KissUser, KissItem
from cicd.rest.response_chain.response_chain_factory import VersionResponseChainFactory

import logging.config
import yaml

from routes.i2_connector_routes import router as i2_connector_router
from routes.kiss_search_routes import router as kiss_search_router

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'logging_config.yml')



with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

load_dotenv(override=True)
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
app.include_router(i2_connector_router)
app.include_router(kiss_search_router)



def clear_connection():
    app.ssh_connection = None
    app.ssh_forward_ctx = None







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


#in de huidge manier van builden werkt dit niet, in de docker container is enkel de source code aanwezig, niet de .git folder!
# Define the version endpoint
# @app.get("/version")
# async def get_version():
#    version_response_chain = VersionResponseChainFactory().create_version_response_chain()
#     version_response = version_response_chain.create_version_response()
#     json_response = version_response.model_dump_json()
#     logger.info("Version response: %s", json_response)
#     return json_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085) #wordt  niet uitgevoerd indien de flask app gestart wordt via docker