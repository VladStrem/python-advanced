from fastapi import FastAPI
from database import Base, engine
from routes.user_views import router as user_router
from routes.spa_views import router as spa_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можна налаштувати на потрібний домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(spa_router)

Base.metadata.create_all(bind=engine)
