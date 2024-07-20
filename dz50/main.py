from fastapi import FastAPI
from models.todo import Base
from database import engine
from routers.todo import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
