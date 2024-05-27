from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from main import get_db
from models import db_models
from schemas.user import AudioCollectionCreate

user_router = APIRouter(prefix="/user")


@user_router.get('/{id}/')
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    print((db_user))
    return db_user


@user_router.post('/{id}/collectables/')
def add_collectable_to_user(id: int, item: AudioCollectionCreate, db: Session = Depends(get_db)):
    db_item = db_models.AudioCollectionDB(**item.dict(), user_id=id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@user_router.get('/{id}/collectables/')
def get_collectable_for_user(id: int, db: Session = Depends(get_db)):
    db_item = db.query(db_models.AudioCollectionDB).filter(db_models.AudioCollectionDB.user_id == id).all()
    return db_item
