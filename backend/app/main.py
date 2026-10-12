from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.router import api_router
import app.models  # Ensure all SQLAlchemy models are registered
from app.database.database import Base, engine, SessionLocal, auto_migrate_sqlite
from app.database.seed import seed_initial_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes database tables on startup, synchronizes columns, and seeds initial goals and skills.
    """
    # Create all tables on startup
    Base.metadata.create_all(bind=engine)

    # Sync SQLite columns if tables existed prior
    auto_migrate_sqlite()

    # Seed initial data
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Personal Skill Learning, Roadmap & Interview Preparation Platform Backend API",
    version=settings.VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the centralized API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """
    Root entrypoint with API information and documentation link.
    """
    return JSONResponse(
        content={
            "app": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "online",
            "docs": "/api/docs",
            "health": f"{settings.API_V1_STR}/health"
        }
    )
