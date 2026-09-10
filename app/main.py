from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import logging
from datetime import datetime
from app.config import settings
from app.models import get_db, Agent, AgentTask, ContentLog
from app.api import agents as agents_routes

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Virtual AI Office",
    description="AI Agents Management System",
    version="0.2.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include agent management routes
app.include_router(agents_routes.router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "0.2.0"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "Virtual AI Office",
        "version": "0.2.0",
        "description": "AI Agents Management System",
        "endpoints": {
            "agents": "/api/agents",
            "health": "/health",
            "docs": "/docs",
            "dashboard": "/dashboard"
        }
    }

# Serve static files (dashboard)
try:
    app.mount("/dashboard", StaticFiles(directory="app/static", html=True), name="dashboard")
except Exception as e:
    logger.warning(f"Dashboard static files not found: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Virtual AI Office 0.2.0 starting...")

    if settings.discord_token:
        logger.info("Discord bot enabled - will start in background")
        try:
            from app.discord_bot import start_discord_bot
            asyncio.create_task(start_discord_bot(settings.discord_token))
        except Exception as e:
            logger.error(f"Failed to start Discord bot: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Virtual AI Office shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
