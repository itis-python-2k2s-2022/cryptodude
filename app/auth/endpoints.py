from datetime import timedelta
import requests

from fastapi import Depends, FastAPI, HTTPException, status, Request, responses, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES, CLIENT_ID
from app.auth.schemas import Token, UserCreate, User
from app.auth.services import get_current_user, authenticate_user, create_access_token
from app.auth.db.services import get_db, get_user_by_email, create_user
from app.auth.db.database import engine
from app.auth.db import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

auth_app = APIRouter(prefix="/auth")

templates = Jinja2Templates(directory="app/auth/templates")


@auth_app.post("/oauth")
async def oauth():
    return responses.RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com"
        f"/auth/userinfo.email "
        f"https://www.googleapis.com/auth/userinfo.profile&include_granted_scopes=true"
        f"&response_type=token&redirect_uri=http://localhost:8000/auth/google_token"
        f"&client_id={CLIENT_ID}"
    )


@auth_app.get("/google_token")
async def get_access_token(request: Request):
    token = request.query_params.get("token")

    if token:
        print(token)
        response = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}")
        userinfo = response.json()
        print(userinfo.get("name"))
        print(userinfo.get("email"))
        return {"message": "ok"}
    return templates.TemplateResponse("get_token.html", {"request": request})


@auth_app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_app.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(db, user)
    return {"status": status.HTTP_201_CREATED}


@auth_app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# TODO переписать
@auth_app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
