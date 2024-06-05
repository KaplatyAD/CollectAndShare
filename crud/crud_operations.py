from sqlalchemy.orm import Session
import schemas.user
from models import db_models


# def create_user(db: Session, user: schemas.user.UserCreate): # old version
#     hashed_password = user.hashed_password + 'hashfunction'
#     db_user = db_models.UserDB(nickname=user.nickname, email=user.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def get_user_by_email(db: Session, email: str):  # проверка существует ли user
    user = db.query(db_models.UserDB).filter(db_models.UserDB.email == email).first()
    return user
