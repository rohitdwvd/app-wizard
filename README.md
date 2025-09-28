# APP-WIZARD

A modular MCP server for identifying addresses from text using various AI providers (OpenAI, Ollama)

## Setup
1. Clone the repo.
2. install requirements via makefile, run
```
make install
or
make install-dev
```
3. Install ollama locally
```
make setup-ollama
```
4. To run 
```
python -m src.main
```
5. Provide json for fields like method, input (text/file/url), provider(model optional)
```
{"id": 1,"method": "identify_addresses","params": {"input": "Contact us at 123 Main St, NYC or visit our LA office at 456 Sunset Blvd","provider": "ollama"}}
or we can provide exact model
{"id": 1,"method": "identify_addresses","params": {"input": "Contact us at 123 Main St, NYC or visit our LA office at 456 Sunset Blvd","provider": "ollama","model": "llama3.2:latest"}}
```

## 🔧 Adding New Providers

To add a new AI provider (e.g., Anthropic Claude, Google Gemini):

1. Create `src/providers/your_provider.py`:
```python
from .base_provider import BaseProvider

class YourProvider(BaseProvider):
    def __init__(self, config):
        super().__init__(config)
        # Initialize your provider
    
    @property
    def provider_name(self) -> str:
        return "your_provider"
    
    def is_available(self) -> bool:
        # Check if provider is configured and available
        pass
    
    def extract_addresses(self, text: str, model=None) -> List[str]:
        # Implement address extraction
        pass
    
    def get_available_models(self) -> List[str]:
        # Return available models
        pass
```

2. Register in `provider_factory.py`:
```python
from .your_provider import YourProvider

# In _initialize_providers method:
self.providers['your_provider'] = YourProvider(self.config.your_provider_config)
```

## 🚀 Usage

```bash
# Start the server
python -m src.main

# Or after installation
app-wizard
```

This modular structure makes it extremely easy to:
- Add new AI providers
- Extend functionality
- Test individual components
- Deploy as a package
- Maintain and scale the codebase

The factory pattern ensures that adding new providers requires minimal changes to existing code!