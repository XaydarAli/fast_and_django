from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from .routers import auth_router
from .routers import posts_router
from fastapi_app.app.schemas import ConfigBase

@AuthJWT.load_config
def get_config():
    return ConfigBase()



app=FastAPI()


@app.get("/")
async def root():
    return {"message":"WELCOME "}



app.include_router(auth_router.router)
app.include_router(posts_router.router)