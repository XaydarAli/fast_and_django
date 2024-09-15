from fastapi import APIRouter,status,HTTPException,Depends
from fastapi_app.app.database import Session,ENGINE
from fastapi_app.app.models import User
from fastapi_app.app.schemas import RegisterSchema,LoginSchema

from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy import or_
session = Session(bind=ENGINE)
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/")
async def auth():
    return {"message":"Authentification router"}









@router.post("/login")
async def login(request:LoginSchema):
    check_user=session.query(User).filter(
        or_(
            User.username==request.username_or_email,
            User.email==request.username_or_email)
    ).first()
    if check_user is not None:
        if check_password_hash(check_user.password,request.password):
            return HTTPException(status_code=status.HTTP_200_OK,detail="Login successful")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")









@router.post("/register")
async def register(request:RegisterSchema):
    check_user=session.query(User).filter(
        or_(User.username==request.username,User.email==request.email)).first()
    if check_user:
        return {"message":"username or email already exists"}


    new_user=User(
        username=request.username,
        email=request.email,
        password=generate_password_hash(request.password),
    )
    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,detail="User registered successfully")



@router.get("/users")
async def users():
    users=session.query(User).all()
    return users


