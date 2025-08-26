import time

import uvicorn
import json
import os
from uuid import UUID

import iris

from datetime import datetime, timedelta, date

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
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

from routes.i2_entiteit_connector_routes import router as i2_entiteit_connector_router
from routes.kiss_search_routes import router as kiss_search_router

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'logging_config.yml')



with open(config_path, 'r') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

load_dotenv(override=True)

async def log_request(request: Request, call_next):
    # Starttijd
    start_time = time.time()

    # Log request details
    logger.info("Request received")
    logger.info("\tmethod: %s", request.method)
    logger.info("\turl: %s", str(request.url))
    logger.info("\theaders: %s", dict(request.headers))
    logger.info("\tremote_addr: %s", request.client.host if request.client else None)

    # Voer de request uit
    response = await call_next(request)

    # Eindtijd
    process_time = (time.time() - start_time) * 1000  # in ms
    logger.info("Response sent")
    logger.info("\tstatus code: %s", response.status_code)
    logger.info("\theaders: %s", dict(response.headers))
    logger.info(f"\tprocessing time (ms): {process_time:.2f}")


    return response


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

app.include_router(i2_entiteit_connector_router)
app.include_router(kiss_search_router)

app.middleware("http")(log_request)

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

# Define the version endpoint
@app.get("/version")
async def get_version():
    version_response_chain = VersionResponseChainFactory().create_version_response_chain()
    version_response = version_response_chain.create_version_response()
    json_response = version_response.model_dump_json()
    logger.info("Version response: %s", json_response)
    return json_response

# Lijst van variabelen die je WEL wil tonen
PUBLIC_ENV_VARS = {
    "KISS_IRIS_IP",
    "KISS_IRIS_PORT",
    "KISS_SCHEMA",
    "KISS_IRIS_ENVIRONMENT",
    "USE_OLD_CACHE_DRIVER",
    "USERS"
}

@app.get("/env")
def get_env():
    public_data = {}
    for key, value in os.environ.items():
        if key in PUBLIC_ENV_VARS and value:
            public_data[key] = value
    return public_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085) #wordt  niet uitgevoerd indien de flask app gestart wordt via docker