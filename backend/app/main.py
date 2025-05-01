# app/main.py

from fastapi import FastAPI
from app.core.middleware import configure_middlewares
from app.core.lifespan import lifespan
from app.routes import api_router

app = FastAPI(
    title="MediHelper 1.0 API", 
    version="1.0", 
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

configure_middlewares(app)
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to MediHelper 1.0 API"}
