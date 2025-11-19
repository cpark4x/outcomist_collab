"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import messages_router
from .api import projects_router
from .api import sessions_router
from .api import streaming
from .api.files import router as files_router
from .config import settings
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Nothing to clean up for now


# Create FastAPI app
app = FastAPI(
    title="Outcomist API",
    description="Multi-project AI workspace backend",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(projects_router)
app.include_router(sessions_router)
app.include_router(messages_router)
app.include_router(files_router)
app.include_router(streaming.router, prefix="/api", tags=["streaming"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "name": "Outcomist API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> dict[str, str | bool]:
    """Health check endpoint for monitoring and load balancers."""
    from datetime import datetime

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "0.1.0",
        "database": "connected",
        "api_key_configured": bool(settings.anthropic_api_key),
    }
