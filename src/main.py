#!/usr/bin/env python3
"""
Main entry point for Address Identification MCP Server
"""

import asyncio

from src.server.mcp_server import MCPServer
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point"""
    config = Config()

    # Log available providers
    logger.info(f"OpenAI available: {config.has_openai}")
    logger.info(f"Ollama URL: {config.get_provider_config('ollama')['base_url']}")

    if not config.has_openai:
        logger.info("No OpenAI API key found. Using Ollama only.")

    server = MCPServer(config)

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped")


if __name__ == "__main__":
    main()
