"""
MCP Server implementation
"""

import asyncio
import json
import sys
from typing import Any, Dict

from ..processors.input_handler import InputHandler
from ..providers.provider_factory import ProviderFactory
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPServer:
    """MCP Server for address identification"""

    def __init__(self, config):
        self.config = config
        self.provider_factory = ProviderFactory(config)
        self.input_handler = InputHandler()
        logger.info("MCP Server initialized")

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "identify_addresses":
                return await self._handle_identify_addresses(params)
            elif method == "list_providers":
                return self._handle_list_providers()
            elif method == "list_models":
                return self._handle_list_models(params)
            elif method == "ping":
                return {"result": "pong"}
            else:
                return {"error": f"Method '{method}' not found", "code": -32601}
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {"error": f"Internal error: {str(e)}", "code": -32603}

    async def _handle_identify_addresses(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle address identification request"""
        input_data = params.get("input", "")
        provider_name = params.get("provider", "auto")
        model = params.get("model")

        if not input_data:
            return {"error": "No input provided", "code": -32602}

        # Process input
        content, input_type = self.input_handler.process_input(input_data)

        if not content:
            return {
                "result": {
                    "input_type": input_type,
                    "provider": provider_name,
                    "addresses": [],
                    "error": "No content found or unable to read input",
                }
            }

        # Extract addresses
        addresses, used_provider = self.provider_factory.extract_addresses(
            content, provider_name, model
        )

        result = {
            "input_type": input_type,
            "provider": used_provider,
            "model": model,
            "addresses": addresses,
            "count": len(addresses),
        }

        logger.info(
            f"Processed {input_type} input with {used_provider}, found {len(addresses)} addresses"
        )

        return {"result": result}

    def _handle_list_providers(self) -> Dict[str, Any]:
        """Handle list providers request"""
        available_providers = self.provider_factory.get_available_providers()
        return {
            "result": {
                "available_providers": available_providers,
                "total_count": len(available_providers),
            }
        }

    def _handle_list_models(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list models request"""
        provider_name = params.get("provider")

        if provider_name:
            provider = self.provider_factory.get_provider(provider_name)
            if provider:
                models = provider.get_available_models()
                return {"result": {"provider": provider_name, "models": models}}
            else:
                return {
                    "error": f"Provider '{provider_name}' not available",
                    "code": -32602,
                }
        else:
            # List models for all providers
            all_models = {}
            for name in self.provider_factory.get_available_providers():
                provider = self.provider_factory.get_provider(name)
                if provider:
                    all_models[name] = provider.get_available_models()

            return {"result": all_models}

    async def run(self):
        """Run the MCP server"""
        logger.info("MCP Server listening for requests...")

        try:
            while True:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )

                if not line:
                    break

                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)

                    if "id" in request:
                        response["id"] = request["id"]

                    print(json.dumps(response))
                    sys.stdout.flush()

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    error_response = {"error": "Parse error", "code": -32700}
                    print(json.dumps(error_response))
                    sys.stdout.flush()

        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Server error: {e}")
