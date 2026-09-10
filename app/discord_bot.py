"""
Discord bot for controlling and communicating with agents.
"""

import discord
from discord.ext import commands
import logging
import json
from datetime import datetime
from app.models import SessionLocal, Agent, AgentTask, AgentMessage
from app.config import settings

logger = logging.getLogger(__name__)

class AgentBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = SessionLocal

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Discord bot logged in as {self.bot.user}")

    @commands.command(name="agents")
    async def list_agents(self, ctx):
        """List all available agents."""
        db = self.db()
        agents = db.query(Agent).all()
        db.close()

        if not agents:
            await ctx.send("❌ No agents configured yet.")
            return

        embed = discord.Embed(
            title="🤖 Available Agents",
            color=discord.Color.blue()
        )

        for agent in agents:
            status_emoji = "🟢" if agent.status == "idle" else "🔴" if agent.status == "error" else "⚙️"
            embed.add_field(
                name=f"{status_emoji} {agent.name}",
                value=f"Type: {agent.agent_type}\nStatus: {agent.status}",
                inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name="agent")
    async def agent_info(self, ctx, agent_name: str):
        """Get detailed info about an agent."""
        db = self.db()
        agent = db.query(Agent).filter(Agent.name == agent_name).first()
        db.close()

        if not agent:
            await ctx.send(f"❌ Agent '{agent_name}' not found.")
            return

        embed = discord.Embed(
            title=f"🤖 {agent.name}",
            description=agent.description or "No description",
            color=discord.Color.blue()
        )

        embed.add_field(name="Type", value=agent.agent_type, inline=True)
        embed.add_field(name="Status", value=agent.status, inline=True)
        embed.add_field(name="Last Activity", value=agent.last_activity or "Never", inline=True)

        if agent.system_prompt:
            embed.add_field(
                name="Instructions",
                value=agent.system_prompt[:200] + "..." if len(agent.system_prompt) > 200 else agent.system_prompt,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="task")
    async def create_task(self, ctx, agent_name: str, task_type: str, *, description: str = None):
        """Create a task for an agent."""
        db = self.db()

        agent = db.query(Agent).filter(Agent.name == agent_name).first()
        if not agent:
            await ctx.send(f"❌ Agent '{agent_name}' not found.")
            db.close()
            return

        task = AgentTask(
            agent_id=agent.id,
            agent_name=agent_name,
            task_type=task_type,
            title=f"{task_type} - {ctx.author.name}",
            description=description or "Task created via Discord",
            status="pending"
        )

        db.add(task)
        db.commit()

        embed = discord.Embed(
            title="✅ Task Created",
            color=discord.Color.green()
        )
        embed.add_field(name="Agent", value=agent_name)
        embed.add_field(name="Task Type", value=task_type)
        embed.add_field(name="Task ID", value=str(task.id))
        embed.add_field(name="Status", value="Pending")

        db.close()
        await ctx.send(embed=embed)

    @commands.command(name="tasks")
    async def list_tasks(self, ctx, agent_name: str = None, status: str = None):
        """List tasks."""
        db = self.db()

        query = db.query(AgentTask)
        if agent_name:
            query = query.filter(AgentTask.agent_name == agent_name)
        if status:
            query = query.filter(AgentTask.status == status)

        tasks = query.order_by(AgentTask.created_at.desc()).limit(10).all()
        db.close()

        if not tasks:
            await ctx.send("📭 No tasks found.")
            return

        embed = discord.Embed(
            title="📋 Recent Tasks",
            color=discord.Color.blue()
        )

        for task in tasks:
            status_emoji = "⏳" if task.status == "pending" else "🟢" if task.status == "completed" else "❌"
            embed.add_field(
                name=f"{status_emoji} {task.title}",
                value=f"Agent: {task.agent_name}\nType: {task.task_type}\nID: {task.id}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="config")
    async def configure_agent(self, ctx, agent_name: str, *, instructions: str):
        """Configure an agent with instructions."""
        db = self.db()

        agent = db.query(Agent).filter(Agent.name == agent_name).first()
        if not agent:
            await ctx.send(f"❌ Agent '{agent_name}' not found.")
            db.close()
            return

        agent.system_prompt = instructions
        agent.updated_at = datetime.utcnow()

        db.commit()

        embed = discord.Embed(
            title="✅ Agent Configured",
            color=discord.Color.green()
        )
        embed.add_field(name="Agent", value=agent_name)
        embed.add_field(name="Instructions Set", value=instructions[:100] + "...", inline=False)

        db.close()
        await ctx.send(embed=embed)

    @commands.command(name="help_agents")
    async def help_command(self, ctx):
        """Show available commands."""
        embed = discord.Embed(
            title="🤖 Agent Commands",
            description="Commands to control and manage agents",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="`!agents`",
            value="List all available agents",
            inline=False
        )
        embed.add_field(
            name="`!agent <name>`",
            value="Get info about a specific agent",
            inline=False
        )
        embed.add_field(
            name="`!task <agent> <type> [description]`",
            value="Create a task for an agent",
            inline=False
        )
        embed.add_field(
            name="`!tasks [agent] [status]`",
            value="List tasks (optionally filtered)",
            inline=False
        )
        embed.add_field(
            name="`!config <agent> <instructions>`",
            value="Configure an agent with instructions",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup_bot(token):
    """Initialize and start the Discord bot."""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Discord bot ready as {bot.user}")

    await bot.add_cog(AgentBot(bot))
    await bot.start(token)

def start_discord_bot(token):
    """Start the Discord bot in a background task."""
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.create_task(setup_bot(token))
