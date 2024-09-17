from fastapi import APIRouter,status,HTTPException,Depends
from fastapi_app.app.database import Session,ENGINE
from fastapi_app.app.models import User
from fastapi_app.app.schemas import RegisterSchema,LoginSchema

from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy import or_
from fastapi_jwt_auth import AuthJWT

from fastapi.encoders import jsonable_encoder


import datetime
session = Session(bind=ENGINE)
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/")
async def auth():
    return {"message":"Authentification router"}









@router.post("/login")
async def login(request:LoginSchema,authorization:AuthJWT=Depends()):
    check_user=session.query(User).filter(
        or_(
            User.username==request.username_or_email,
            User.email==request.username_or_email)
    ).first()
    if check_user is not None:
        if check_password_hash(check_user.password,request.password):
            access_token=authorization.create_access_token(subject=request.username_or_email,expires_time=datetime.timedelta(minutes=3))
            refresh_token=authorization.create_refresh_token(subject=request.username_or_email,expires_time=datetime.timedelta(days=1))
            response={
                "status":200,
                "detail":"User logged in",
                "access_token":access_token,
                "refresh_token":refresh_token,


            }

            return jsonable_encoder(response)
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")






@router.get("/token/verify")
async def auth_logout_user(authorization:AuthJWT=Depends()):
    try:
        authorization.jwt_required()
    except Exception as e:
        return HTTPException(status_code=401,detail="Token INValid")
    return {"detail":"token is valid "}


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
    data=[
        {
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "created_at":user.created_at
        }
        for user in users
    ]
    return jsonable_encoder(data)


