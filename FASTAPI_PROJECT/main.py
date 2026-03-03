
from fastapi import FastAPI
from database import engine, Base
from app.blog.routes import router as blog_router
from app.blog import models
from app.brand import models
from app.brand.routes import router as brand_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(blog_router)
app.include_router(brand_router)