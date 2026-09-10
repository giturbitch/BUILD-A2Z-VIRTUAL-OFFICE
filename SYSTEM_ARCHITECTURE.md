# Virtual AI Office - System Architecture v0.2

## Overview

The Virtual AI Office is an **interactive agent management system** where you control multiple AI agents via Discord, assign them specific tasks, and monitor their progress in real-time.

Instead of agents running on fixed schedules, they now:
1. Wait for instructions (tasks) from you
2. Execute specific work based on your configuration
3. Report back with results
4. Store everything in a database for tracking

## Core Components

### 1. **Agent Management System**
- **Agents**: Autonomous workers (Social Media, Website Builder, Prospector, etc.)
- **Tasks**: Specific work items assigned to agents
- **Configurations**: Instructions that teach agents how to behave
- **Messages**: Chat history with agents for transparency

### 2. **Discord Bot Integration**
- Interactive commands to control agents
- Real-time task status updates
- Agent configuration via Discord
- Conversation history

### 3. **FastAPI Backend**
- RESTful API for programmatic control
- WebSocket for real-time updates
- Database for persistent state
- Agent execution engine

### 4. **Database Schema**

```
Agents
├── id, name, type (social_media, website, ghl_prospecting)
├── status (idle, busy, error)
├── system_prompt (instructions for agent)
├── credentials (encrypted API keys, passwords)
└── config (agent-specific settings)

AgentTasks
├── id, agent_id, task_type
├── status (pending, running, completed, failed)
├── title, description, instructions
├── parameters (task-specific data)
├── result, error (output)
└── created_at, started_at, completed_at

AgentMessages
├── id, agent_id
├── direction (incoming/outgoing)
├── sender, message, message_type
└── context (related task_id, data)

ContentLog
├── id, agent_name, platform
├── content, status (draft, posted)
├── task_id (which task created this)
└── created_at, posted_at

IntegrationCredentials
├── platform (instagram, linkedin, twitter, ghl, discord)
├── credential_type (api_key, oauth_token, username_password)
└── value (encrypted)
```

## How It Works

### Agent Lifecycle

```
1. CREATE AGENT
   !task social_media create_agent
   → Agent created, status: idle

2. CONFIGURE
   !config social_media "You are an expert..."
   → Agent learns what to do

3. ASSIGN TASK
   !task social_media post_content Create Instagram post...
   → Task created, status: pending

4. EXECUTE
   Agent picks up task from queue
   status: running
   → Generates content using Llama 3.1 + system prompt

5. COMPLETE
   Task finished
   status: completed
   result: {content generated}
   → Logged to ContentLog

6. REPORT
   Discord update: "Task #123 completed ✓"
   → User sees result
```

## Agent Types

### Social Media Agent
**Purpose**: Generate and post content to social platforms

**Configuration**: 
- Style preferences (casual, professional, punchy)
- Platform rules (character limits, hashtags)
- Content topics (automation, SaaS, growth)

**Tasks**:
- `post_content` - Generate a single post
- `schedule_posts` - Plan weekly content
- `reply_to_comments` - Engage with audience

**Output**: Posts (Instagram, LinkedIn, Twitter)

### Website Building Agent
**Purpose**: Create websites when triggered by client events

**Configuration**:
- Design preferences (colors, layout)
- Standard sections (services, pricing, testimonials)
- CMS templates to use

**Tasks**:
- `create_website` - Build site for new client
- `update_website` - Modify existing site
- `add_portfolio` - Add client work examples

**Triggers**: Email notification → "New appointment booked" → Agent creates site

**Output**: Website mockup → Mark contact as "website_done"

### GHL Prospecting Agent
**Purpose**: Find opportunities and automate outreach

**Configuration**:
- Who to target (lead score threshold, company size)
- Outreach message templates
- Follow-up sequences

**Tasks**:
- `scan_leads` - Find new qualified prospects
- `qualify_lead` - Score and evaluate opportunity
- `send_outreach` - Message potential client
- `follow_up` - Send sequences

**Output**: Qualified leads → Messages sent → Engagement tracked

### Email/CRM Agent
**Purpose**: Automate email sequences and lead nurturing

**Tasks**:
- `send_campaign` - Email to segment
- `sequence_automation` - Multi-step nurture
- `lead_scoring` - Evaluate prospects

## API Usage Examples

### Create Agent
```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "social_media",
    "agent_type": "social_media",
    "description": "Posts to Instagram, LinkedIn, Twitter",
    "system_prompt": "You are a social media expert for SaaS companies..."
  }'
```

### Assign Task
```bash
curl -X POST http://localhost:8000/api/agents/social_media/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "post_content",
    "title": "Instagram Post - Automation Benefits",
    "description": "Create engaging post about business automation",
    "instructions": "Use 2-3 emojis, include hashtags, 150-200 words",
    "parameters": {
      "platform": "instagram",
      "topic": "business automation",
      "style": "casual and engaging"
    },
    "priority": 2
  }'
```

### Check Task Status
```bash
curl http://localhost:8000/api/agents/tasks/123
```

### Get Agent Messages
```bash
curl http://localhost:8000/api/agents/social_media/messages
```

### Configure Agent
```bash
curl -X PATCH http://localhost:8000/api/agents/social_media \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "You are now an expert in video content creation...",
    "config": {
      "posting_frequency": "3x daily",
      "best_times": ["9:00", "12:00", "18:00"]
    }
  }'
```

## Discord Commands

| Command | Usage | Purpose |
|---------|-------|---------|
| `!agents` | `!agents` | List all agents |
| `!agent` | `!agent social_media` | Agent details |
| `!task` | `!task social_media post_content "Create post..."` | Assign task |
| `!tasks` | `!tasks social_media` | List tasks |
| `!config` | `!config social_media "You are..."` | Configure agent |
| `!messages` | `!messages social_media` | Chat history |
| `!content` | `!content social_media instagram` | View generated content |

## Workflow Examples

### Example 1: Daily Social Media Posts

```
Morning: !agents
         Check status of all agents

         !task social_media post_content "Morning post about lead generation"
         !task social_media post_content "Thread about CRM automation"
         !task social_media post_content "LinkedIn tip: email integration"

Monitor: !tasks social_media running
         Watch as they generate content

Check:   !content social_media
         Review what was created

Post:    When ready, approve and post to platforms
```

### Example 2: New Client Onboarding

```
Trigger: Email notification in GHL - "New appointment: ABC Corp"

1. !task website create_website "Client: ABC Corp, Real estate, needs listings page"
2. Agent generates mockup
3. System marks contact as "website_mockup_done"
4. You review in Discord
5. If approved: Schedule actual website build

Or automated:
- Webhook from GHL → Task created → Agent builds → Notified in Discord
```

### Example 3: Continuous Prospecting

```
Setup: !config ghl_prospecting "Find real estate companies in [region], score leads..."

Continuous:
- Agent scans GHL every hour
- Finds high-potential leads
- Sends personalized outreach
- Tracks responses
- Follows up automatically

You see: Real-time Discord updates
         "Found 3 qualified leads, sent outreach to 5 prospects"
```

## Security Considerations

### Credential Storage
- Never share credentials in Discord messages
- Use API endpoint to store securely:
  ```bash
  curl -X POST http://localhost:8000/api/agents/social_media/credentials \
    -H "Content-Type: application/json" \
    -d '{
      "platform": "instagram",
      "credential_type": "username_password",
      "username": "...",
      "password": "..."
    }'
  ```

### Environment Variables
- All API keys in `.env` file (never committed)
- Discord token kept secure
- Database URLs protected

### Task Isolation
- Each task runs independently
- Credentials isolated per platform
- Audit log of all actions

## Monitoring & Debugging

### View All Agent Activity
```bash
curl http://localhost:8000/api/agents/
```

### Track Specific Task
```bash
curl http://localhost:8000/api/agents/tasks/123
```

### Agent Logs
```bash
# Check server console/logs
tail -f logs/agent_activity.log
```

### Discord Notifications
- Real-time task updates in Discord
- Error notifications
- Completion summaries

## What's Different from v0.1?

| Feature | v0.1 | v0.2 |
|---------|------|------|
| Execution | Schedule-based (cron) | Task-based (on-demand) |
| Control | Dashboard UI | Discord + API |
| Configuration | Hard-coded prompts | Dynamic via commands |
| Interaction | None (auto-run) | Full chat interface |
| Tracking | Basic logs | Detailed message history |
| Status | Limited info | Real-time updates |
| Credentials | Stored in env | Secure storage system |
| Extensibility | Limited | Highly extensible |

## Next Steps

1. **Set up Discord bot** (see SETUP_DISCORD_BOT.md)
2. **Create your first agent**: `!task social_media create_agent`
3. **Configure it**: `!config social_media "..."`
4. **Assign tasks**: `!task social_media post_content "..."`
5. **Connect platforms**: Add credentials for actual posting
6. **Automate**: Set up webhooks and triggers

## Roadmap

- [ ] Real-time WebSocket updates
- [ ] Automated GoHighLevel integration
- [ ] Email notification triggers
- [ ] Credential encryption
- [ ] Agent performance analytics
- [ ] Custom agent templates
- [ ] Multi-user support
- [ ] Audit logging
