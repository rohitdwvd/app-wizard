"""
Factory for creating AI providers
"""

from typing import List, Optional

from ..utils.logger import setup_logger
from .base_provider import BaseProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider

logger = setup_logger(__name__)


class ProviderFactory:
    """Factory class for creating and managing AI providers"""

    def __init__(self, config):
        self.config = config
        self.providers = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all available providers"""

        # OpenAI Provider
        if self.config.openai_config.get("api_key"):
            try:
                self.providers["openai"] = OpenAIProvider(self.config.openai_config)
                if self.providers["openai"].is_available():
                    logger.info("OpenAI provider registered")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI provider: {e}")

        # Ollama Provider
        try:
            self.providers["ollama"] = OllamaProvider(self.config.ollama_config)
            if self.providers["ollama"].is_available():
                logger.info("Ollama provider registered")
            else:
                logger.warning("Ollama provider not available")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama provider: {e}")

    def get_provider(self, provider_name: str) -> Optional[BaseProvider]:
        """Get a specific provider by name"""
        provider = self.providers.get(provider_name)
        if provider and provider.is_available():
            return provider
        return None

    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [
            name for name, provider in self.providers.items() if provider.is_available()
        ]

    def get_best_available_provider(self) -> Optional[BaseProvider]:
        """Get the best available provider (OpenAI first, then others)"""
        if "openai" in self.providers and self.providers["openai"].is_available():
            return self.providers["openai"]

        for provider in self.providers.values():
            if provider.is_available():
                return provider

        return None

    def extract_addresses(
        self, text: str, provider_name: str = "auto", model: Optional[str] = None
    ) -> tuple[List[str], str]:
        """Extract addresses using specified provider"""
        if provider_name == "auto":
            provider = self.get_best_available_provider()
            if not provider:
                logger.error("No providers available")
                return [], "none"
        else:
            provider = self.get_provider(provider_name)
            if not provider:
                logger.error(f"Provider '{provider_name}' not available")
                return [], provider_name

        addresses = provider.extract_addresses(text, model)
        return addresses, provider.provider_name
