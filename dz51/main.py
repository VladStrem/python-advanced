from fastapi import FastAPI
from database import Base, engine
from routes.user_views import router as user_router

app = FastAPI()
app.include_router(user_router)
Base.metadata.create_all(bind=engine)
