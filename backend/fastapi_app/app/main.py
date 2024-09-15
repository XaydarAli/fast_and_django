from fastapi import FastAPI
from .routers import auth_router
from .routers import posts_router
app=FastAPI()

@app.get("/")
async def root():
    return {"message":"WELCOME "}



app.include_router(auth_router.router)
app.include_router(posts_router.router)