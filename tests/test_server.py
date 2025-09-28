"""
Tests for MCP server
"""

import unittest

from src.server.mcp_server import MCPServer
from src.utils.config import Config


class TestMCPServer(unittest.TestCase):
    """Test MCP server functionality"""

    def setUp(self):
        self.config = Config()
        self.server = MCPServer(self.config)

    def test_server_initialization(self):
        self.assertIsInstance(self.server, MCPServer)
        self.assertIsNotNone(self.server.provider_factory)
        self.assertIsNotNone(self.server.input_handler)

    async def test_ping_request(self):
        request = {"method": "ping", "id": 1}
        response = await self.server.handle_request(request)
        self.assertEqual(response["result"], "pong")

    async def test_invalid_method(self):
        request = {"method": "invalid_method", "id": 1}
        response = await self.server.handle_request(request)
        self.assertEqual(response["code"], -32601)


if __name__ == "__main__":
    unittest.main()
