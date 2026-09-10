# Virtual AI Office - Claude Development Guide

## Project Overview

This is an autonomous AI agent platform for a SaaS agency. It runs independent agents on schedules to handle:
- Social media posting (Instagram, LinkedIn, X)
- Website building (via GoHighLevel)
- Lead management and tracking
- Client fulfillment automation

## Tech Stack

- **Backend**: Python 3.9+, FastAPI, SQLAlchemy
- **Frontend**: HTML/CSS/JavaScript (simple dashboard)
- **AI**: Llama 3.1 via Ollama (local, free, no API costs)
- **Automation**: Playwright, Selenium
- **Database**: SQLite (dev), PostgreSQL (production)

## Project Structure

```
app/
├── agents/          # All autonomous agents
│   ├── base_agent.py
│   ├── social_media_agent.py
│   └── website_agent.py
├── static/          # Dashboard UI
├── config.py        # Configuration
├── database.py      # Database models
├── main.py          # FastAPI app
└── scheduler.py     # Agent scheduling

run.py              # Entry point
requirements.txt    # Dependencies
```

## Running the Project

1. **Install Ollama** (one-time):
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3.1
   ```

2. **Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Start Ollama** (in a separate terminal):
   ```bash
   ollama serve
   ```

4. **Run**:
   ```bash
   python run.py
   ```

5. **Access**:
   - Dashboard: http://localhost:8000/dashboard
   - API Docs: http://localhost:8000/docs

## Key Files to Know

- `app/agents/social_media_agent.py` - Main social content generation
- `app/scheduler.py` - When agents run
- `app/static/index.html` - Dashboard interface
- `app/config.py` - Environment configuration

## Making Changes

### To modify agent schedules:
Edit `app/scheduler.py` → `initialize()` method

### To change social media content prompts:
Edit `app/agents/social_media_agent.py` → `generate_platform_content()` method

### To add a new agent:
1. Create new file in `app/agents/`
2. Inherit from `BaseAgent`
3. Implement `async def run()`
4. Register in `app/scheduler.py`

## Current Status

- ✅ Core framework complete
- ✅ Social Media Agent (content generation ready, posting in draft mode)
- ✅ Website Agent (framework ready, integration pending)
- ✅ Dashboard UI (monitoring ready)
- ✅ Scheduling system (autonomous runs ready)
- ⏳ Social media credentials (waiting for user to provide)
- ⏳ HighLevel browser automation (pending)

## Next Priority Tasks

1. Add social media login credentials
2. Implement actual posting to Instagram/LinkedIn/X
3. Add HighLevel browser automation for website building
4. Connect CRM agent for lead tracking
5. Deploy to VPS

## Important Notes

- All credentials should be in `.env` (never commit to git)
- Database is SQLite locally, will migrate to PostgreSQL for VPS
- Agents run asynchronously and independently
- Dashboard auto-refreshes every 30 seconds
- All agent runs are logged to the database

## Testing

```bash
# Test social media agent
curl -X POST http://localhost:8000/agents/social_media/run

# Get all agent status
curl http://localhost:8000/agents/status

# View recent tasks
curl http://localhost:8000/tasks
```
