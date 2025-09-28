"""
Tests for provider implementations
"""

import unittest
from unittest.mock import patch

from src.providers.ollama_provider import OllamaProvider
from src.providers.openai_provider import OpenAIProvider
from src.providers.provider_factory import ProviderFactory
from src.utils.config import Config


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI provider"""

    def setUp(self):
        self.config = {"api_key": "test-key"}

    @patch("src.providers.openai_provider.OpenAI")
    def test_provider_initialization(self, mock_openai):
        provider = OpenAIProvider(self.config)
        self.assertTrue(provider.is_available())
        self.assertEqual(provider.provider_name, "openai")

    def test_provider_without_key(self):
        config = {"api_key": None}
        provider = OpenAIProvider(config)
        self.assertFalse(provider.is_available())


class TestOllamaProvider(unittest.TestCase):
    """Test Ollama provider"""

    def setUp(self):
        self.config = {"base_url": "http://localhost:11434", "default_model": "llama2"}

    def test_provider_initialization(self):
        provider = OllamaProvider(self.config)
        self.assertEqual(provider.provider_name, "ollama")
        self.assertEqual(provider.base_url, "http://localhost:11434")


class TestProviderFactory(unittest.TestCase):
    """Test provider factory"""

    def setUp(self):
        self.config = Config()

    def test_factory_initialization(self):
        factory = ProviderFactory(self.config)
        self.assertIsInstance(factory, ProviderFactory)


if __name__ == "__main__":
    unittest.main()
