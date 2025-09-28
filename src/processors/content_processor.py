"""
Content processing utilities for cleaning and extracting text
"""

import re

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentProcessor:
    """Handles content cleaning and processing"""

    @staticmethod
    def clean_html_content(html_content: str) -> str:
        """Clean HTML content by removing scripts, CSS, and other non-content elements"""
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")

            # Remove script and style elements
            for element in soup(["script", "style", "meta", "link", "noscript"]):
                element.decompose()

            # Remove CSS and JS file references
            for tag in soup.find_all(attrs={"href": re.compile(r"\.(css|js)$", re.I)}):
                tag.decompose()

            for tag in soup.find_all(attrs={"src": re.compile(r"\.(css|js)$", re.I)}):
                tag.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            return ContentProcessor._truncate_content(text, 10000)

        except ImportError:
            logger.warning("BeautifulSoup not available, using basic extraction")
            return ContentProcessor.basic_text_extraction(html_content)
        except Exception as e:
            logger.error(f"Error cleaning HTML content: {e}")
            return html_content[:5000]

    @staticmethod
    def basic_text_extraction(html_content: str) -> str:
        """Basic text extraction without BeautifulSoup"""
        # Remove script and style tags
        html_content = re.sub(
            r"<script[^>]*>.*?</script>",
            "",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        html_content = re.sub(
            r"<style[^>]*>.*?</style>",
            "",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove HTML tags
        html_content = re.sub(r"<[^>]+>", "", html_content)

        # Clean whitespace
        html_content = re.sub(r"\s+", " ", html_content).strip()

        return ContentProcessor._truncate_content(html_content, 8000)

    @staticmethod
    def _truncate_content(content: str, max_length: int) -> str:
        """Truncate content if too long"""
        if len(content) > max_length:
            content = content[:max_length] + "... [content truncated]"
            logger.info(f"Content truncated to {max_length} characters")
        return content
