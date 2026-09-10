from abc import ABC, abstractmethod
from datetime import datetime
import logging
import requests
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.model = settings.ollama_model
        self.ollama_url = settings.ollama_base_url
        self.last_run = None
        self.next_run = None

    @abstractmethod
    async def run(self) -> dict:
        """Execute the agent's main task. Must be implemented by subclasses."""
        pass

    def generate_content(self, prompt: str, system_prompt: str = None) -> str:
        """Use Llama 3.1 via Ollama to generate content."""
        try:
            # Build the full prompt with system context
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")

            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            error_msg = f"Cannot connect to Ollama at {self.ollama_url}. Is Ollama running? Start with: ollama serve"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Content generation error: {str(e)}")
            raise

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
