from fastapi import APIRouter, HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from typing_extensions import Annotated
from security.model.security_model import User
from routes.kiss_search_routes import get_current_active_user
from service.personen_service import PersonenService
from response.personen_marshaller import PersonenMarshaller

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/person")
#def test123(current_user: Annotated[User, Depends(get_current_active_user)], param1: str, param2: str):
def person_by_name(name: str):    
    personen_service = PersonenService()
    personen_marshaller = PersonenMarshaller()
    logger.info('Look persons by name: %s', name)

    result = personen_service.get_personen_by_name(name=name)
    
    json_result = personen_marshaller.marshal_result(personen=result)
    return JSONResponse(content=json_result)
    