"""
Configuration management
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the MCP server"""

    def __init__(self):
        self.openai_config = {"api_key": os.getenv("OPENAI_API_KEY")}

        self.ollama_config = {
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "default_model": os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
        }

        # Add more provider configs here
        self.anthropic_config = {"api_key": os.getenv("ANTHROPIC_API_KEY")}

        self.google_config = {"api_key": os.getenv("GOOGLE_API_KEY")}

    @property
    def has_openai(self) -> bool:
        return bool(self.openai_config["api_key"])

    @property
    def has_ollama(self) -> bool:
        # Will be checked dynamically by the provider
        return True

    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """Get configuration for a specific provider"""
        configs = {
            "openai": self.openai_config,
            "ollama": self.ollama_config,
            "anthropic": self.anthropic_config,
            "google": self.google_config,
        }
        return configs.get(provider_name, {})
