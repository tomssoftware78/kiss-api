from fastapi import APIRouter, HTTPException, Request, Query
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from dotenv import dotenv_values

from typing_extensions import Annotated
from security.model.security_model import User
from routes.kiss_search_routes import get_current_active_user
from service.personen_service import PersonenService
from service.entiteiten_service import EntiteitenService
from response.personen_marshaller import PersonenMarshaller
from dao.kiss_data_export.entiteiten_dao import EntiteitenDao

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export/entiteiten")
def get_entiteiten(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste IdEntiteit uit vorige batch, of 0 voor de eerste batch"),
):
    entiteiten_dao = EntiteitenDao()

    result = entiteiten_dao.get_entiteiten_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)

@router.get("/export/entiteit/personen/count")
def persoon_count(request: Request):
    entiteiten_dao = EntiteitenDao()

    count = entiteiten_dao.get_personen_count()

    return {
        "count": count
    }

@router.get("/export/entiteit/personen")
def get_personen(
    page_size: int = Query(..., description="Aantal records per batch"),
    last_id: int = Query(..., description="Laatste IdEntiteit uit vorige batch, of 0 voor de eerste batch"),
):
    entiteiten_dao = EntiteitenDao()

    result = entiteiten_dao.get_personen_paged(page_size=page_size, last_id=last_id)
    #logger.debug(type(result))
    #logger.debug(result)
    
    return JSONResponse(content=result)

