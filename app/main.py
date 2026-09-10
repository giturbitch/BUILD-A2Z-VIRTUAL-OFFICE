from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import logging
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db, AgentTask
from app.scheduler import AgentScheduler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Virtual AI Office", description="AI Agents for Agency Automation")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AgentScheduler()

# Models
class AgentRunRequest(BaseModel):
    agent_name: str

class AgentStatusResponse(BaseModel):
    name: str
    last_run: datetime = None
    next_run: datetime = None

# Routes
@app.on_event("startup")
async def startup_event():
    """Start the scheduler on app startup."""
    asyncio.create_task(scheduler.start())
    logger.info("Virtual AI Office started")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the scheduler on app shutdown."""
    await scheduler.stop()
    logger.info("Virtual AI Office stopped")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "scheduler_running": scheduler.running
    }

@app.get("/agents/status")
async def get_agents_status():
    """Get status of all agents."""
    return await scheduler.get_all_status()

@app.get("/agents/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """Get status of a specific agent."""
    status = await scheduler.get_agent_status(agent_name)
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    return status

@app.post("/agents/{agent_name}/run")
async def run_agent_now(agent_name: str):
    """Manually trigger an agent to run now."""
    result = await scheduler.run_agent_now(agent_name)
    if result.get("status") == "failed":
        raise HTTPException(status_code=500, detail=result.get("error"))
    return result

@app.get("/tasks")
async def get_recent_tasks(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent agent task history."""
    tasks = db.query(AgentTask).order_by(AgentTask.created_at.desc()).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}")
async def get_task_detail(task_id: int, db: Session = Depends(get_db)):
    """Get details of a specific task."""
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/")
async def root():
    """Root endpoint - serves dashboard info."""
    return {
        "app": "Virtual AI Office",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "agents": "/agents/status",
            "tasks": "/tasks",
            "dashboard": "/dashboard"
        }
    }

# Serve static files (dashboard)
try:
    app.mount("/dashboard", StaticFiles(directory="app/static", html=True), name="dashboard")
except Exception as e:
    logger.warning(f"Dashboard static files not found: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
