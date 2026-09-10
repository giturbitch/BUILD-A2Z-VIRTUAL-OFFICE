# Discord Bot Setup Guide

The Virtual AI Office now includes a Discord bot for interactive agent management and real-time updates.

## Step 1: Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Give it a name: "Virtual AI Office"
4. Go to **Bot** section
5. Click **Add Bot**
6. Copy the **TOKEN** - you'll need this for .env

## Step 2: Configure Bot Permissions

1. In Developer Portal, go to **OAuth2** → **URL Generator**
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Embed Links
   - Read Messages/View Channels
   - Read Message History
4. Copy the generated URL and invite the bot to your Discord server

## Step 3: Add Discord Token to .env

```bash
DISCORD_TOKEN=your_bot_token_here
```

## Step 4: Start the Server

```bash
python run.py
```

When the server starts, you'll see: `Discord bot logged in as [BotName]`

## Using the Discord Bot

### Available Commands

**`!agents`** - List all available agents
```
!agents
```

**`!agent <name>`** - Get info about a specific agent
```
!agent social_media
```

**`!task <agent> <type> [description]`** - Create a task for an agent
```
!task social_media post_content Create Instagram post about new service
```

**`!tasks [agent] [status]`** - List tasks
```
!tasks social_media pending
!tasks
```

**`!config <agent> <instructions>`** - Configure an agent with instructions
```
!config social_media You are a social media expert for SaaS companies. Always include emojis and call-to-actions in posts.
```

**`!help_agents`** - Show all available commands

## Example Workflow

### 1. Create a Social Media Agent

In Discord:
```
!task social_media create_agent Configure for Instagram posting
```

### 2. Configure the Agent

```
!config social_media You are an expert Instagram copywriter. Create engaging posts about: business automation, agency growth, SaaS tips. Always include 3-5 relevant hashtags and a call-to-action.
```

### 3. Give It a Task

```
!task social_media post_content Create a post about lead generation automation
```

### 4. Monitor Progress

```
!tasks social_media running
```

## Setting Up Specific Agents

### Social Media Agent

Configure with:
```
!config social_media You are a social media expert for a SaaS agency. Create viral posts about: website building, CRM automation, lead generation, business growth. Style: casual on Instagram, professional on LinkedIn, punchy on Twitter. Always include strong CTAs and relevant hashtags.
```

Then give tasks:
```
!task social_media post_content Create Instagram post about CRM benefits
!task social_media post_content Create LinkedIn post about agency automation
!task social_media post_content Create Twitter post about lead generation
```

### Website Building Agent

Configure with:
```
!config website You are a website builder. When given a client email or contact info, create a professional website design mock-up based on their industry. Include layout, colors, and key sections.
```

Give it a task:
```
!task website create_website Client: Acme Corp, Real estate company, needs professional site with property listings
```

### GHL Prospecting Agent

Configure with:
```
!config ghl_prospecting You are a lead prospector. Scan GoHighLevel for opportunities: qualified leads, recent activity, engagement patterns. Recommend outreach strategies and reach out to high-potential prospects with personalized messages.
```

This agent runs continuously to find opportunities.

## Storing Credentials

For sensitive credentials (Instagram login, GoHighLevel API key, etc.):

```
POST /api/agents/{agent_name}/credentials
{
  "platform": "instagram",
  "credential_type": "username_password",
  "username": "your_username",
  "password": "your_password"
}
```

Or via Discord:
```
!creds instagram username_password your_username your_password
```

## Viewing Agent Activity

Check recent agent messages:
```
!messages social_media
```

View generated content:
```
!content social_media instagram
```

## API Endpoints

You can also interact with agents via API:

```bash
# List all agents
curl http://localhost:8000/api/agents

# Create an agent
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "social_media",
    "agent_type": "social_media",
    "description": "Posts to Instagram, LinkedIn, Twitter"
  }'

# Create a task
curl -X POST http://localhost:8000/api/agents/social_media/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "post_content",
    "title": "Create Instagram post",
    "description": "Create engaging post about automation"
  }'

# Check task status
curl http://localhost:8000/api/agents/tasks/1

# Send message to agent
curl -X POST http://localhost:8000/api/agents/social_media/messages \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "user123",
    "message": "Create a post about our new pricing"
  }'
```

## Troubleshooting

**Bot not responding in Discord:**
- Check that token is correct in `.env`
- Make sure bot is invited to your server
- Check server logs for errors

**No permissions to send messages:**
- Go to Developer Portal
- OAuth2 → URL Generator
- Make sure "Send Messages" permission is selected
- Re-invite bot with new link

**Can't find agents:**
- Create agents first via API or `!task` command
- Check they appear with `!agents`

## Next Steps

1. Set up your Discord server with the bot
2. Create your first agent: `!task social_media create_agent`
3. Configure it with instructions: `!config social_media ...`
4. Start assigning tasks and watch it work
5. Connect platform credentials for actual posting
6. Set up GoHighLevel integration for prospects
