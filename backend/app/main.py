# FastAPI entrypoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import router as api_v1_router
from config import settings
from database import engine
from models.database_models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NOSS Hybrid RAG Backend",
    description="National Occupational Skills Standard Curriculum Generation System with JWT Authentication and SQLite Database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "NOSS Hybrid RAG Backend Ready",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "JWT Authentication",
            "SQLite Database",
            "Document Management", 
            "Template Management",
            "Chat Management",
            "Token Usage Tracking",
            "Admin Dashboard"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "noss-backend",
        "database": "sqlite",
        "authentication": "jwt"
    }
