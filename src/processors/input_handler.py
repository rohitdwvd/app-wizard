"""
Input handling for different input types (text, file, URL)
"""

import os
from typing import Tuple
from urllib.parse import urlparse

import requests

from ..utils.logger import setup_logger
from .content_processor import ContentProcessor

logger = setup_logger(__name__)


class InputHandler:
    """Handles different types of input (text, file, URL)"""

    def __init__(self):
        self.content_processor = ContentProcessor()

    def process_input(self, input_data: str) -> Tuple[str, str]:
        """Process input and return (content, input_type)"""
        if self._is_file_path(input_data):
            return self._read_file(input_data), "file"
        elif self._is_valid_url(input_data):
            return self._fetch_url(input_data), "url"
        else:
            return input_data, "text"

    def _is_file_path(self, path: str) -> bool:
        """Check if string is a valid file path"""
        return os.path.isfile(path)

    def _is_valid_url(self, url: str) -> bool:
        """Check if string is a valid URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _process_file_content(self, content: str, file_path: str) -> str:
        """Process file content, cleaning HTML if it's an HTML file"""
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension in [".html", ".htm"]:
            logger.info(f"Processing HTML file: {file_path}")
            return self.content_processor.clean_html_content(content)
        elif file_extension in [".txt", ".md", ".json"]:
            return self.content_processor._truncate_content(content, 10000)
        else:
            # For other files, treat as plain text but truncate more aggressively
            return self.content_processor._truncate_content(content, 8000)

    def _read_file(self, file_path: str) -> str:
        """Read content from a file with smart processing"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            processed_content = self._process_file_content(raw_content, file_path)
            logger.info(f"Successfully read and processed file: {file_path}")
            return processed_content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""

    def _fetch_url(self, url: str) -> str:
        """Fetch content from a URL with smart content processing"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, timeout=15, headers=headers, stream=True)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "").lower()

            if "text/html" in content_type:
                cleaned_content = self.content_processor.clean_html_content(
                    response.text
                )
                logger.info(f"Successfully fetched and cleaned HTML from URL: {url}")
                return cleaned_content
            elif "text/" in content_type:
                content = response.text
                content = self.content_processor._truncate_content(content, 10000)
                logger.info(f"Successfully fetched text from URL: {url}")
                return content
            else:
                logger.warning(f"Unsupported content type: {content_type}")
                return ""

        except Exception as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return ""
