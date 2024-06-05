from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_users_db_sqlalchemy import access_token
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
import db
from crud.crud_operations import get_user_by_email
from db.database import get_db

from models.db_models import UserDB
from schemas.user import User, Token, UserCreate
from config import SECRET_KEY, ALGORITHM

auth = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


@auth.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_func(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=404, detail="User already exists")
    create_user = UserDB(nickname=user.nickname, email=user.email,
                         hashed_password=bcrypt_context.hash(user.hashed_password))
    db.add(create_user)
    db.commit()
    return create_user


@auth.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(user.nickname, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(nickname: str, password: str, db):
    user = db.query(UserDB).filter(UserDB.nickname == nickname).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(nickname: str, user_id: int, expires_delta: timedelta = None):
    encode = {'sub': nickname, 'id': user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nickname: str = payload.get('sub')
        user_id: int = payload.get('id')
        if nickname is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        print('print from get cur user')
        return {'user_id': user_id, 'username': nickname}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
