from sqlalchemy.orm import Session
import schemas.user
from models import db_models


def create_user(db: Session, user: schemas.user.User):
    hashed_password = user.password + 'hashfunction'
    db_user = db_models.User(nickname=user.nickname, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()