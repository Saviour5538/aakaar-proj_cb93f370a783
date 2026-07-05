import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router
from backend.routes.conversations import router as conversations_router
from database.config import get_db, Base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database initialization
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database initialization failed: {str(e)}")

# FastAPI application setup
app = FastAPI(
    title="DocMind",
    description="AI-powered document management and conversational assistant",
    version="1.0.0",
)

# CORS middleware setup
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Lifespan context manager for startup/shutdown
@app.on_event("startup")
async def startup_event():
    init_db()

@app.on_event("shutdown")
async def shutdown_event():
    pass  # Add any necessary cleanup logic here

# Router inclusion
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")

# Auto-mounted AI router — ai/routes.py exposes /api/ai/* (it carries its own prefix)
from ai.routes import router as ai_router
app.include_router(ai_router)
