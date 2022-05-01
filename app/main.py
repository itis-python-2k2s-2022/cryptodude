from fastapi import FastAPI

from app.auth.endpoints import auth_app

app = FastAPI()

app.include_router(auth_app)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
