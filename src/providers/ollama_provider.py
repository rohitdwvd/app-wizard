"""
Ollama provider implementation
"""

from typing import List, Optional

import requests

from ..utils.logger import setup_logger
from .base_provider import BaseProvider

logger = setup_logger(__name__)


class OllamaProvider(BaseProvider):
    """Ollama provider for address extraction"""

    def __init__(self, config):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.default_model = config.get("default_model", "llama3.2:1b")
        logger.info(f"Ollama provider initialized with URL: {self.base_url}")

    @property
    def provider_name(self) -> str:
        return "ollama"

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            response.raise_for_status()
            return True
        except:
            return False

    def get_available_models(self) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            model_names = [
                model.get("name", "") for model in models if model.get("name")
            ]
            logger.info(f"Available Ollama models: {model_names}")
            return model_names
        except Exception as e:
            logger.error(f"Error fetching Ollama models: {e}")
            return []

    def extract_addresses(self, text: str, model: Optional[str] = None) -> List[str]:
        if not self.is_available():
            logger.error("Ollama is not accessible")
            return []

        try:
            model_name = model or self.default_model
            available_models = self.get_available_models()

            if available_models and model_name not in available_models:
                logger.warning(
                    f"Model '{model_name}' not found. Using: {available_models[0]}"
                )
                model_name = (
                    available_models[0] if available_models else self.default_model
                )

            prompt = self.get_address_extraction_prompt(text)

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 500},
            }

            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=120
            )
            response.raise_for_status()

            result = response.json()
            addresses_text = result.get("response", "").strip()

            if not addresses_text or addresses_text == "No addresses found":
                return []

            addresses = [
                addr.strip() for addr in addresses_text.split("\n") if addr.strip()
            ]
            logger.info(f"Ollama ({model_name}) found {len(addresses)} addresses")
            return addresses

        except Exception as e:
            logger.error(f"Error with Ollama address extraction: {e}")
            return []
