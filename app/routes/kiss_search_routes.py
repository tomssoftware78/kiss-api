import logging
import os
import json
from jose import JWTError, jwt
from fastapi import APIRouter, HTTPException
from typing_extensions import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, date

from model import Item, KissCase, KissUser, KissItem
from security.model.security_model import TokenData, Token, User
from service.kiss_search_service import KissSearchService
from security.security_service import SecurityService
from service.gebruikers_service import GebruikersService

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

security_service = SecurityService(SECRET_KEY, ALGORITHM)
fake_users_db = json.loads(os.environ.get('USERS'))


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



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@router.post("/token", response_model=Token)
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

@router.get("/case/{case_id}", response_model=KissCase)
def get_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    term = ((str)(case_id))
    term = term[0:2]+"/" + term[2:]
    return search_kiss_case(current_user, term, badge_id)[0]

@router.post("/case/search", response_model=list[KissCase])
def search_kiss_case(current_user: Annotated[User, Depends(get_current_active_user)], term: str, badge_id: int):
    cases = []
    
    kiss_search_service = KissSearchService()
    cases = kiss_search_service.search_kiss_case(term=term, badge_id=badge_id)

    return cases

@router.get("/items/{case_id}", response_model=list[KissItem])
def get_kiss_items_from_case(current_user: Annotated[User, Depends(get_current_active_user)], case_id: int, badge_id: int):
    items = []

    kiss_search_service = KissSearchService()
    items = kiss_search_service.get_kiss_items_from_case(case_id=case_id, badge_id=badge_id)

    return items
    

@router.post("/items", response_model=list[KissItem])
def get_kiss_items(current_user: Annotated[User, Depends(get_current_active_user)], item_ids: list[int], badge_id: int):
    items = []

    kiss_search_service = KissSearchService()
    items = kiss_search_service.items(item_ids=item_ids, badge_id=badge_id)

    return items

@router.get("/user/{badge_id}", response_model=KissUser)
async def get_kiss_user(current_user: Annotated[User, Depends(get_current_active_user)], badge_id: int):
    
    gebruikers_service = GebruikersService()

    user = gebruikers_service.get_user(badge_id=badge_id)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User " + str(badge_id) + " not found")
