import os
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
import logging
from src.config import (
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_MAX_TOKENS,
    SYSTEM_MESSAGE,
)

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = AsyncOpenAI(api_key=api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=60))
    async def call_openai_api(self, prompt: str, model: str = OPENAI_MODEL):
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt},
                ],
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}", exc_info=True)
            raise
