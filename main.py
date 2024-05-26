import uvicorn
from fastapi import FastAPI, templating, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
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
    print(db_user.collection)
    return db_user


@app.get('/user/{id}/')
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get('/username/{name}/')
def get_user_by_name(nickname: str, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.nickname == nickname).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get('/users/')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(db_models.UserDB).all()
    return users


@app.post('/user/{id}/collectables/')
def add_collectable_to_user(id: int, item: AudioCollectionCreate, db: Session = Depends(get_db)):
    db_item = db_models.AudioCollectionDB(**item.dict(), user_id=id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get('/login/')
def get_user(nickname: str, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.nickname == nickname).first()
    print(db_user)
    return db_user


@app.get("/hello/{name}/")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
