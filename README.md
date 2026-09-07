# 🤖 Virtual AI Office - Agency Automation Platform

A comprehensive AI-powered agent platform that automates your entire SaaS agency backend. Deploy autonomous agents to handle social media, website building, lead management, and client fulfillment—so you can focus on closing deals.

## 🎯 Features

### Current (MVP)
- **Social Media Agent** - Generates and posts content to Instagram, LinkedIn, and X (Twitter)
- **Website Building Agent** - Automates website creation and management via GoHighLevel
- **Autonomous Scheduling** - Agents run on intelligent schedules (9am, 12pm, 3pm, 6pm, etc.)
- **Real-time Dashboard** - Monitor all agents, view task history, and trigger runs manually
- **RESTful API** - Full API access for all agent operations

### Planned
- HighLevel CRM integration (messages, email campaigns, lead tracking)
- Advanced content templates and variations
- Performance analytics (views, engagement, conversions)
- Multi-account management
- A/B testing for social media posts
- Lead scoring and qualification
- Automated client onboarding workflows

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- An Anthropic API key
- GoHighLevel API key (optional, for website agent)
- Social media credentials (you'll provide these later)

### Setup

1. **Clone and setup environment:**
```bash
cd /home/user/BUILD-A2Z-VIRTUAL-OFFICE
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
GHL_API_KEY=pit-74d72ffb-b759-46ec-bf64-8215b261601d
```

3. **Start the server:**
```bash
python run.py
```

4. **Access the dashboard:**
- Dashboard UI: http://localhost:8000/dashboard
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📋 Architecture

### Components

**Backend (FastAPI)**
- Main API server with async support
- Task scheduling and execution
- Database for task history and logs
- RESTful endpoints for agent control

**Agents**
- `BaseAgent` - Abstract base class for all agents
- `SocialMediaAgent` - Content generation and social posting
- `WebsiteAgent` - Website automation via Playwright
- `Scheduler` - Manages agent execution schedules

**Frontend Dashboard**
- Real-time agent status monitoring
- Manual trigger controls
- Task history viewer
- Statistics and analytics

**Database**
- SQLite for local development
- Tables: AgentTasks, AgentSchedules, ContentLogs
- Ready to migrate to PostgreSQL for VPS deployment

## 🎮 Using the Dashboard

### Agent Status Panel
- See last run time for each agent
- Click "Run Now" to manually trigger an agent
- Visual indicators for running/idle/error states

### Quick Actions
- **Run Social Media Agent** - Generate and post content now
- **Run Website Agent** - Execute website building tasks
- **Refresh Data** - Force update all statistics

### Recent Tasks
- View last 10 tasks and their results
- Filter by agent, status, or date
- Track content posted and leads generated

## 🔌 API Endpoints

### Agent Control
```
GET  /agents/status              - Get all agents status
GET  /agents/{name}/status       - Get specific agent status
POST /agents/{name}/run          - Trigger agent immediately
```

### Tasks & History
```
GET  /tasks                      - Get recent tasks (paginated)
GET  /tasks/{id}                 - Get task details
```

### System
```
GET  /health                     - Health check
GET  /                           - API info
```

## 📊 Agent Schedules

**Social Media Agent**
- 9:00 AM - Instagram post
- 12:00 PM - LinkedIn post
- 3:00 PM - X (Twitter) posts
- 6:00 PM - Instagram post

**Website Agent**
- 8:00 AM - Daily website sync and updates

*Schedules can be customized in `app/scheduler.py`*

## 🔐 Security Notes

- Never commit `.env` file with real credentials
- Use environment variables for all secrets
- Social media credentials stored securely
- API keys are validated on startup

## 📦 What's Included

```
BUILD-A2Z-VIRTUAL-OFFICE/
├── app/
│   ├── agents/
│   │   ├── base_agent.py       # Abstract base agent class
│   │   ├── social_media_agent.py
│   │   └── website_agent.py
│   ├── static/
│   │   └── index.html          # Dashboard UI
│   ├── config.py               # Configuration management
│   ├── database.py             # SQLAlchemy models
│   ├── main.py                 # FastAPI app
│   └── scheduler.py            # Agent scheduling
├── run.py                       # Entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .env.example                # Example configuration
```

## 🛠️ Development

### Adding a New Agent

1. Create a new file in `app/agents/`:
```python
from app.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MyAgent")
    
    async def run(self) -> dict:
        # Your agent logic here
        return {"status": "completed"}
```

2. Register in `app/scheduler.py`:
```python
self.agents = {
    "social_media": SocialMediaAgent(),
    "website": WebsiteAgent(),
    "my_agent": MyAgent(),  # Add here
}
```

3. Add schedule in `initialize()` method

### Local Testing

```bash
# Test an agent
curl http://localhost:8000/agents/social_media/run

# Get status
curl http://localhost:8000/agents/status

# View tasks
curl http://localhost:8000/tasks
```

## 📈 Next Steps

1. **Add Social Media Credentials** - Once you're ready, provide Instagram, LinkedIn, and X login info
2. **Customize Content** - Adjust prompts in `SocialMediaAgent` for your brand voice
3. **Configure Schedules** - Set posting times that match your audience timezone
4. **Deploy to VPS** - Instructions coming for production deployment
5. **Add More Agents** - CRM, email, analytics agents

## 🤝 Contributing

This is your custom platform. Feel free to:
- Modify agent prompts and behavior
- Add new agents for other tasks
- Customize dashboard UI
- Integrate additional APIs

## 📞 Support

For issues or questions:
1. Check logs in the dashboard
2. Review API error responses
3. Check `/health` endpoint status

## 📄 License

Private - Your agency's proprietary system

---

**Built with:** FastAPI • Claude AI • Playwright • SQLAlchemy

**Version:** 0.1.0 (MVP)