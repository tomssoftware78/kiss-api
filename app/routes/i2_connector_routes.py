from fastapi import APIRouter, HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing_extensions import Annotated
from security.model.security_model import User
from routes.kiss_search_routes import get_current_active_user

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/test123")
#def test123(current_user: Annotated[User, Depends(get_current_active_user)], param1: str, param2: str):
def test123(param1: str, param2: str):    
    logger.info('test123')
    logger.info('param1: %s', param1)
    logger.info('param2: %s', param2)

    return {
        'key1': 'value1',
        'key2': 'value2'
    }