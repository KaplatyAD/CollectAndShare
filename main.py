import uvicorn
from typing import Annotated
from fastapi import FastAPI, templating, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from starlette.templating import Jinja2Templates
from crud.crud_operations import get_user_by_email
from models import db_models
from routes.user_routes import user_router
from db.database import SessionLocal, engine, get_db
from schemas.user import User, UserCreate, AudioCollection, AudioCollectionCreate
from auth.auth import auth, get_current_user

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(auth)
templates = Jinja2Templates(directory="templates")

db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get('/')
def home_page():
    return {"message": "API для веб приложения, помогающего организовать свою аудио библиотеку"}


@app.get('/username/{name}/', response_model=User)
def get_user_by_name(nickname: str, db: Session = Depends(get_db)):
    db_user = db.query(db_models.UserDB).filter(db_models.UserDB.nickname == nickname).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get('/users/', response_model=list[User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(db_models.UserDB).all()
    return users


# @app.get('/login/', response_class=HTMLResponse)
# def login_page(request: Request):
#     return templates.TemplateResponse('login.html', {"request": request})
#
@app.get('/login', tags=['auth'])
def login(user: user_dependency):
    print('test')
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    print('login')
    return {"user": user}



if __name__ == "__main__":
    uvicorn.run('main:app', port=8001, reload=True)
