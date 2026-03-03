from fastapi import FastAPI
from database import engine, Base
from app.blog.routes import router as blog_router
from app.blog import models  # IMPORTANT: ensures table is registered

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(blog_router)