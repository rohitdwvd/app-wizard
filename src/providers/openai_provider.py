"""
OpenAI provider implementation
"""

from typing import List, Optional

from openai import OpenAI

from ..utils.logger import setup_logger
from .base_provider import BaseProvider

logger = setup_logger(__name__)


class OpenAIProvider(BaseProvider):
    """OpenAI provider for address extraction"""

    def __init__(self, config):
        super().__init__(config)
        self.client = None
        self.default_model = "gpt-3.5-turbo"

        if self.is_available():
            self.client = OpenAI(api_key=config.get("api_key"))
            logger.info("OpenAI provider initialized")

    @property
    def provider_name(self) -> str:
        return "openai"

    def is_available(self) -> bool:
        return bool(self.config.get("api_key"))

    def get_available_models(self) -> List[str]:
        if not self.is_available():
            return []
        return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]

    def extract_addresses(self, text: str, model: Optional[str] = None) -> List[str]:
        if not self.client:
            logger.error("OpenAI client not initialized")
            return []

        try:
            model_name = model or self.default_model
            prompt = self.get_address_extraction_prompt(text)

            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise address extraction agent.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=500,
            )

            addresses_text = response.choices[0].message.content.strip()

            if addresses_text == "No addresses found":
                return []

            addresses = [
                addr.strip() for addr in addresses_text.split("\n") if addr.strip()
            ]
            logger.info(f"OpenAI found {len(addresses)} addresses")
            return addresses

        except Exception as e:
            logger.error(f"Error with OpenAI address extraction: {e}")
            return []
