import uvicorn
from fastapi import FastAPI, templating, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from crud.crud_operations import create_user, get_user_by_email
from models import db_models

from db.database import SessionLocal, engine
from schemas.user import User, UserCreate, AudioCollection, AudioCollectionCreate

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/login/')
def create_user_func(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db_models.UserDB(nickname=user.nickname, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





@app.get('/username/{name}/', response_model=User)
def get_user_by_name(nickname: str, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.nickname == nickname).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    print((db_user))
    return db_user


@app.get('/users/', response_model=list[User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(db_models.UserDB).all()
    return users





@app.get('/login/')
def get_user(nickname: str, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.nickname == nickname).first()
    print(db_user)
    return db_user




if __name__ == "__main__":
    uvicorn.run('main:app', port=8001, reload=True)
