from abc import ABC, abstractmethod
from datetime import datetime
import logging
from anthropic import Anthropic
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.last_run = None
        self.next_run = None

    @abstractmethod
    async def run(self) -> dict:
        """Execute the agent's main task. Must be implemented by subclasses."""
        pass

    def generate_content(self, prompt: str, system_prompt: str = None) -> str:
        """Use Claude to generate content."""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def log_task(self, status: str, result: str = None, error: str = None):
        """Log agent execution for monitoring."""
        self.last_run = datetime.utcnow()
        logger.info(f"[{self.name}] Status: {status} | Result: {result} | Error: {error}")

    async def execute(self) -> dict:
        """Wrapper for error handling and logging."""
        try:
            self.log_task("running")
            result = await self.run()
            self.log_task("completed", result=str(result))
            return {"status": "success", "data": result}
        except Exception as e:
            error_msg = str(e)
            self.log_task("failed", error=error_msg)
            logger.error(f"[{self.name}] Error: {error_msg}")
            return {"status": "failed", "error": error_msg}
