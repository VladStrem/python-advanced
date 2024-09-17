from fastapi import FastAPI
from database import Base, engine
from routes.user_views import router as user_router
from routes.posts import router as post_router

app = FastAPI()

app.include_router(post_router, prefix="/posts")
app.include_router(user_router)

Base.metadata.create_all(bind=engine)
