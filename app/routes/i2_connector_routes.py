from fastapi import APIRouter, HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing_extensions import Annotated
from main import User
from main import get_current_active_user

router = APIRouter()

@router.get("/test123")
def test123(current_user: Annotated[User, Depends(get_current_active_user)], param1: int, param2: int):
    print('test123')
    print('param1: ', param1)
    print('param2: ', param2)
    return {
        'key1': 'value1',
        'key2': 'value2'
    }