import uvicorn
from fastapi import FastAPI, templating, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from starlette.templating import Jinja2Templates
from crud.crud_operations import create_user, get_user_by_email
from models import db_models
from routes.user_routes import user_router
from db.database import SessionLocal, engine, get_db
from schemas.user import User, UserCreate, AudioCollection, AudioCollectionCreate

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)

templates = Jinja2Templates(directory="templates")


@app.get('/')
def home_page():
    return {"message": "API для веб приложения, помогающего организовать свою аудио библиотелку"}


@app.post('/register/')
def create_user_func(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=404, detail="User already exists")
    return create_user(db, user)


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
# @app.post('/login/')
# def login_page(request: Request, username: str = Form()):
#
#     return templates.TemplateResponse('login.html', {"request": request})


if __name__ == "__main__":
    uvicorn.run('main:app', port=8001, reload=True)
