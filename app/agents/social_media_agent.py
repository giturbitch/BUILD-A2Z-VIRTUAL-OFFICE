import asyncio
import logging
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.config import settings
from app.database import SessionLocal, ContentLog

logger = logging.getLogger(__name__)

class SocialMediaAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SocialMediaAgent")
        self.platforms = ["instagram", "linkedin", "twitter"]

    async def run(self) -> dict:
        """Generate and post content to all platforms."""
        results = {}

        for platform in self.platforms:
            try:
                content = await self.generate_platform_content(platform)
                if content:
                    posted = await self.post_to_platform(platform, content)
                    status = "posted" if posted else "draft"

                    self.log_content_to_db(platform, content, status)

                    results[platform] = {
                        "status": status,
                        "content": content[:100] + "..." if len(content) > 100 else content
                    }
                else:
                    results[platform] = {"status": "failed", "error": "Content generation failed"}
            except Exception as e:
                logger.error(f"Error posting to {platform}: {str(e)}")
                results[platform] = {"status": "failed", "error": str(e)}

        return results

    async def generate_platform_content(self, platform: str) -> str:
        """Generate platform-specific content using Llama 3.1."""
        prompts = {
            "instagram": """Generate an engaging Instagram post for a SaaS agency that helps businesses with:
- Website building
- Google Business optimization
- CRM integration (using GoHighLevel)
- Lead tracking and management
- Email campaigns

Make it casual, engaging, with relevant emojis and a call-to-action. Include 3-5 relevant hashtags.
Keep it under 2200 characters.""",

            "linkedin": """Generate a professional LinkedIn post for a SaaS agency CEO sharing insights about:
- Scaling agencies with automation
- The importance of CRM integration
- Lead management best practices
- Business growth strategies

Make it thought-provoking, industry-focused. Include a clear message and subtle call-to-action.
Keep it under 1300 characters.""",

            "twitter": """Generate an engaging X/Twitter post about:
- Business automation
- Lead generation tips
- SaaS industry insights
- Agency growth hacks

Make it punchy, witty, and shareable. Include 1-2 relevant hashtags.
Keep it under 280 characters."""
        }

        system_prompt = f"You are a expert copywriter creating viral {platform} content that drives engagement and leads for a SaaS agency."

        try:
            content = self.generate_content(
                prompt=prompts.get(platform, "Generate engaging social media content."),
                system_prompt=system_prompt
            )
            return content
        except Exception as e:
            logger.error(f"Content generation failed for {platform}: {str(e)}")
            return None

    async def post_to_platform(self, platform: str, content: str) -> bool:
        """Post content to the specified platform. Currently in draft mode."""
        logger.info(f"[DRAFT MODE] Generated content for {platform}: {content[:80]}...")
        return False

    def log_content_to_db(self, platform: str, content: str, status: str):
        """Log generated content to the database."""
        try:
            db = SessionLocal()
            log_entry = ContentLog(
                agent_name="social_media",
                platform=platform,
                content=content,
                status=status,
                created_at=datetime.utcnow()
            )
            db.add(log_entry)
            db.commit()
            db.close()
            logger.info(f"Logged {platform} content to database (status: {status})")
        except Exception as e:
            logger.error(f"Failed to log content to database: {str(e)}")

    async def schedule_posts(self):
        """Schedule posts at optimal times."""
        posting_times = {
            "instagram": [10, 14, 18],
            "linkedin": [9, 12],
            "twitter": [8, 10, 12, 14, 16, 18]
        }
        return posting_times
