from fastapi import FastAPI
from app.database import create_database
from app.routes.auth import router as auth_router
from app.routes.chat import router as chat_router

app = FastAPI()

create_database()

@app.get("/")
def home():
    return {"mensagem": "API do Alinyo pronta!"}

app.include_router(auth_router)

app.include_router(chat_router)