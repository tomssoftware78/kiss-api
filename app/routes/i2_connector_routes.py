from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from dotenv import dotenv_values

from typing_extensions import Annotated
from security.model.security_model import User
from routes.kiss_search_routes import get_current_active_user
from service.personen_service import PersonenService
from response.personen_marshaller import PersonenMarshaller

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/person")
def person_by_name(request: Request):
    logger.debug('/person')

    client_ip = request.client.host
    query_params = dict(request.query_params)
    naam = query_params['naam']
    voornaam = query_params['voornaam']
    
    logging.info(f"ontvangst van {client_ip} met parameters: {query_params}")

    personen_service = PersonenService()
    personen_marshaller = PersonenMarshaller()
    logger.info('test')
    logger.info('Look persons by name: %s', naam)
    logger.info('test1')

    result = personen_service.get_personen_by_name(naam=naam, voornaam=voornaam)
    
    json_result = personen_marshaller.marshal_result(personen=result)
    return JSONResponse(content=json_result)

@router.get("/person/expand")
def person_by_name(request: Request):
    logger.debug('/person/expand')

    json_result = {}

    client_ip = request.client.host
    query_params = dict(request.query_params)
    id = query_params['id']

    personen_service = PersonenService()
    result = personen_service.expand_persoon(id=id)

    return JSONResponse(content=result)


@router.get("/env")
def get_env():
    # Read from .env file
    env_values = dotenv_values(".env")  # Returns a dict
    return env_values
    