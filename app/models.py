from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Agent(Base):
    """Agent configuration and state."""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    agent_type = Column(String)  # social_media, website, ghl_prospecting, etc
    status = Column(String, default="idle")  # idle, busy, error
    description = Column(Text, nullable=True)

    system_prompt = Column(Text, nullable=True)  # Instructions for agent
    credentials = Column(JSON, nullable=True)  # Platform credentials, API keys, etc
    config = Column(JSON, nullable=True)  # Agent-specific settings

    last_activity = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgentTask(Base):
    """Tasks assigned to agents."""
    __tablename__ = "agent_tasks"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, index=True)
    agent_id = Column(Integer, index=True)

    task_type = Column(String)  # post_content, create_website, send_message, etc
    title = Column(String)
    description = Column(Text)

    status = Column(String, default="pending")  # pending, running, completed, failed
    priority = Column(Integer, default=0)  # 0=low, 1=normal, 2=high

    instructions = Column(Text, nullable=True)  # Specific instructions for this task
    parameters = Column(JSON, nullable=True)  # Task-specific data
    result = Column(Text, nullable=True)  # What happened
    error = Column(Text, nullable=True)  # If failed, why

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgentMessage(Base):
    """Messages sent to/from agents (chat history)."""
    __tablename__ = "agent_messages"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, index=True)
    agent_name = Column(String, index=True)

    direction = Column(String)  # incoming (user->agent) or outgoing (agent->user)
    sender = Column(String)  # who sent it (username, discord_id, system, etc)

    message = Column(Text)
    message_type = Column(String, default="text")  # text, command, status_update, etc

    context = Column(JSON, nullable=True)  # Related task_id, data, etc

    created_at = Column(DateTime, default=datetime.utcnow)

class ContentLog(Base):
    """Generated content (posts, etc)."""
    __tablename__ = "content_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, index=True)
    platform = Column(String)
    content_type = Column(String)  # post, draft, message, etc

    content = Column(Text)
    status = Column(String, default="draft")  # draft, posted, scheduled, failed

    posted_at = Column(DateTime, nullable=True)
    engagement_count = Column(Integer, default=0)

    task_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

class IntegrationCredential(Base):
    """Store platform credentials securely."""
    __tablename__ = "integration_credentials"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)  # instagram, linkedin, twitter, ghl, discord, etc
    agent_name = Column(String, index=True)

    credential_type = Column(String)  # api_key, oauth_token, username/password, etc
    value = Column(Text)  # Actually encrypted in production

    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
