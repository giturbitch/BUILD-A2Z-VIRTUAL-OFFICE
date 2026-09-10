"""
Agent management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.models import get_db, Agent, AgentTask, AgentMessage, ContentLog

router = APIRouter(prefix="/api/agents", tags=["agents"])

class AgentCreate(BaseModel):
    name: str
    agent_type: str
    description: Optional[str] = None
    system_prompt: Optional[str] = None

class AgentUpdate(BaseModel):
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    status: Optional[str] = None
    config: Optional[dict] = None

class TaskCreate(BaseModel):
    task_type: str
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    parameters: Optional[dict] = None
    priority: int = 0

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

@router.get("/")
async def list_agents(db: Session = Depends(get_db)):
    """List all agents."""
    agents = db.query(Agent).all()
    return agents

@router.post("/")
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent."""
    existing = db.query(Agent).filter(Agent.name == agent.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Agent '{agent.name}' already exists")

    db_agent = Agent(
        name=agent.name,
        agent_type=agent.agent_type,
        description=agent.description,
        system_prompt=agent.system_prompt,
        status="idle"
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/{agent_name}")
async def get_agent(agent_name: str, db: Session = Depends(get_db)):
    """Get agent details."""
    agent = db.query(Agent).filter(Agent.name == agent_name).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return agent

@router.patch("/{agent_name}")
async def update_agent(agent_name: str, update: AgentUpdate, db: Session = Depends(get_db)):
    """Update agent configuration."""
    agent = db.query(Agent).filter(Agent.name == agent_name).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    if update.description is not None:
        agent.description = update.description
    if update.system_prompt is not None:
        agent.system_prompt = update.system_prompt
    if update.status is not None:
        agent.status = update.status
    if update.config is not None:
        agent.config = update.config

    agent.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(agent)
    return agent

@router.get("/{agent_name}/tasks")
async def get_agent_tasks(agent_name: str, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all tasks for an agent."""
    query = db.query(AgentTask).filter(AgentTask.agent_name == agent_name)
    if status:
        query = query.filter(AgentTask.status == status)
    tasks = query.order_by(AgentTask.created_at.desc()).all()
    return tasks

@router.post("/{agent_name}/tasks")
async def create_task(agent_name: str, task: TaskCreate, db: Session = Depends(get_db)):
    """Create a task for an agent."""
    agent = db.query(Agent).filter(Agent.name == agent_name).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    db_task = AgentTask(
        agent_id=agent.id,
        agent_name=agent_name,
        task_type=task.task_type,
        title=task.title,
        description=task.description,
        instructions=task.instructions,
        parameters=task.parameters,
        priority=task.priority,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task details."""
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/tasks/{task_id}")
async def update_task(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
    """Update task status."""
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if update.status is not None:
        task.status = update.status
        if update.status == "running" and not task.started_at:
            task.started_at = datetime.utcnow()
        elif update.status == "completed":
            task.completed_at = datetime.utcnow()

    if update.result is not None:
        task.result = update.result
    if update.error is not None:
        task.error = update.error

    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

@router.get("/{agent_name}/messages")
async def get_agent_messages(agent_name: str, limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history with an agent."""
    messages = db.query(AgentMessage).filter(
        AgentMessage.agent_name == agent_name
    ).order_by(AgentMessage.created_at.desc()).limit(limit).all()
    return list(reversed(messages))

@router.post("/{agent_name}/messages")
async def send_message_to_agent(agent_name: str, sender: str, message: str, db: Session = Depends(get_db)):
    """Send a message to an agent."""
    agent = db.query(Agent).filter(Agent.name == agent_name).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    msg = AgentMessage(
        agent_id=agent.id,
        agent_name=agent_name,
        direction="incoming",
        sender=sender,
        message=message,
        message_type="text"
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.get("/{agent_name}/content")
async def get_agent_content(agent_name: str, platform: Optional[str] = None, limit: int = 20, db: Session = Depends(get_db)):
    """Get content generated by an agent."""
    query = db.query(ContentLog).filter(ContentLog.agent_name == agent_name)
    if platform:
        query = query.filter(ContentLog.platform == platform)
    content = query.order_by(ContentLog.created_at.desc()).limit(limit).all()
    return content
