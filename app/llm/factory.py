import os
from app.llm.base import LLMProvider

def get_llm_provider() -> LLMProvider:
    """
    Factory: reads LLM_PROVIDER from env and returns the right implementation.
    This is the single switch point — change .env, not code.
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        from app.llm.gemini_provider import GeminiProvider
        return GeminiProvider()
    elif provider == "ollama":
        from app.llm.ollama_provider import OllamaProvider
        return OllamaProvider()
    elif provider == "openai":
        from app.llm.openai_provider import OpenAIProvider
        return OpenAIProvider()
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")