"""
Base provider interface for AI models
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseProvider(ABC):
    """Abstract base class for AI providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available and configured"""
        pass

    @abstractmethod
    def extract_addresses(self, text: str, model: Optional[str] = None) -> List[str]:
        """Extract addresses from text"""
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get provider name"""
        pass

    def get_address_extraction_prompt(self, text: str) -> str:
        """Get the standard prompt for address extraction"""
        return f"""You are an expert address identification agent that works with multiple languages and formats.

TASK: Extract ALL physical addresses from the text, regardless of language or format.

INSTRUCTIONS:
1. Look for addresses in ANY language (English, Spanish, French, German, Chinese, Japanese, Arabic, Hindi, etc.)
2. Recognize various address formats:
   - US format: 123 Main St, City, State ZIP
   - UK format: 123 High Street, City, Postcode
   - European format: Street Name 123, ZIP City
   - Asian formats with building/district names
   - Any format with street numbers, names, and location identifiers

3. Include addresses that contain:
   - Street numbers and names
   - Building names with numbers
   - Apartment/Unit numbers
   - City, state/province, postal/zip codes
   - Country names (if present)

4. IMPORTANT: Return ONLY the addresses, one per line, without any additional text, numbering, or formatting.
5. If no addresses are found, return exactly: "No addresses found"

TEXT TO ANALYZE:
{text}

ADDRESSES:"""
