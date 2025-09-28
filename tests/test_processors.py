"""
Tests for content processors
"""

import unittest

from src.processors.content_processor import ContentProcessor
from src.processors.input_handler import InputHandler


class TestContentProcessor(unittest.TestCase):
    """Test content processing"""

    def test_basic_text_extraction(self):
        html = '<html><head><script>alert("test")</script></head><body><p>Hello World</p></body></html>'
        result = ContentProcessor.basic_text_extraction(html)
        self.assertIn("Hello World", result)
        self.assertNotIn("alert", result)

    def test_content_truncation(self):
        long_text = "a" * 15000
        result = ContentProcessor._truncate_content(long_text, 10000)
        self.assertTrue(len(result) <= 10000 + 50)  # Account for truncation message


class TestInputHandler(unittest.TestCase):
    """Test input handling"""

    def setUp(self):
        self.handler = InputHandler()

    def test_text_input(self):
        content, input_type = self.handler.process_input("This is plain text")
        self.assertEqual(input_type, "text")
        self.assertEqual(content, "This is plain text")

    def test_url_detection(self):
        self.assertTrue(self.handler._is_valid_url("https://example.com"))
        self.assertFalse(self.handler._is_valid_url("not-a-url"))


if __name__ == "__main__":
    unittest.main()
