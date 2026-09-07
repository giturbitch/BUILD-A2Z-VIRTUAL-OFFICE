import asyncio
import schedule
import logging
from datetime import datetime
from app.agents.social_media_agent import SocialMediaAgent
from app.agents.website_agent import WebsiteAgent

logger = logging.getLogger(__name__)

class AgentScheduler:
    def __init__(self):
        self.agents = {
            "social_media": SocialMediaAgent(),
            "website": WebsiteAgent(),
        }
        self.running = False
        self.tasks = []

    async def initialize(self):
        """Set up all agent schedules."""
        # Social Media Agent - runs multiple times daily
        schedule.every().day.at("09:00").do(self._schedule_agent_run, "social_media")
        schedule.every().day.at("12:00").do(self._schedule_agent_run, "social_media")
        schedule.every().day.at("15:00").do(self._schedule_agent_run, "social_media")
        schedule.every().day.at("18:00").do(self._schedule_agent_run, "social_media")

        # Website Agent - runs once daily
        schedule.every().day.at("08:00").do(self._schedule_agent_run, "website")

        logger.info("Agent schedules initialized")

    def _schedule_agent_run(self, agent_name: str):
        """Schedule an agent to run."""
        task = asyncio.create_task(self.agents[agent_name].execute())
        self.tasks.append(task)
        logger.info(f"Scheduled {agent_name} to run at {datetime.now()}")

    async def start(self):
        """Start the scheduler."""
        self.running = True
        logger.info("Agent scheduler started")
        await self.initialize()

        while self.running:
            schedule.run_pending()
            await asyncio.sleep(60)  # Check every minute

    async def stop(self):
        """Stop the scheduler."""
        self.running = False
        logger.info("Agent scheduler stopped")

    async def run_agent_now(self, agent_name: str) -> dict:
        """Manually trigger an agent run."""
        if agent_name not in self.agents:
            return {"status": "failed", "error": f"Agent {agent_name} not found"}

        try:
            result = await self.agents[agent_name].execute()
            logger.info(f"Manual run of {agent_name} completed: {result}")
            return result
        except Exception as e:
            logger.error(f"Manual run of {agent_name} failed: {str(e)}")
            return {"status": "failed", "error": str(e)}

    async def get_agent_status(self, agent_name: str) -> dict:
        """Get status of an agent."""
        if agent_name not in self.agents:
            return {"status": "not_found"}

        agent = self.agents[agent_name]
        return {
            "name": agent_name,
            "last_run": agent.last_run,
            "next_run": agent.next_run,
        }

    async def get_all_status(self) -> dict:
        """Get status of all agents."""
        statuses = {}
        for agent_name in self.agents:
            statuses[agent_name] = await self.get_agent_status(agent_name)
        return statuses
