from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Abstract interface all LLM providers must implement.
    Lets us swap Gemini / Ollama / OpenAI without touching agent code.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Send a prompt to the LLM and return the raw text response."""
        pass