"""AI providers — Groq, DeepSeek, OpenRouter (no Azure).

All three expose an OpenAI-compatible chat completions API.
DeepSeek and OpenRouter share the openai SDK with different base_urls.
Groq has its own SDK (or can also use openai-compatible).
"""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod

import requests

from ..config import settings

log = logging.getLogger(__name__)


class AIProvider(ABC):
    """Base class for all AI providers."""

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        *,
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: dict | None = None,
    ) -> str:
        """Send a chat completion request and return the assistant message text."""
        ...

    def chat_json(
        self,
        messages: list[dict],
        *,
        model: str = "",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> dict:
        """Send a chat request expecting JSON output. Parses and returns dict."""
        text = self.chat(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        # Try to extract JSON from the response (handle markdown fences)
        cleaned = text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first and last fence lines
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines)
        return json.loads(cleaned)


class _OpenAICompatible(AIProvider):
    """Shared base for providers that use the OpenAI-compatible chat API."""

    def __init__(self, base_url: str, api_key: str, default_model: str):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._default_model = default_model

    def chat(self, messages, *, model="", temperature=0.7, max_tokens=4096, response_format=None):
        url = f"{self._base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        body = {"model": model or self._default_model, "messages": messages,
                "temperature": temperature, "max_tokens": max_tokens}
        if response_format:
            body["response_format"] = response_format
        resp = requests.post(url, headers=headers, json=body, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


class DeepSeekProvider(_OpenAICompatible):
    def __init__(self):
        super().__init__(
            base_url=settings.deepseek_base_url or "https://api.deepseek.com",
            api_key=settings.deepseek_api_key,
            default_model=settings.deepseek_model or "deepseek-chat",
        )


class OpenRouterProvider(_OpenAICompatible):
    def __init__(self):
        super().__init__(
            base_url=settings.openrouter_base_url or "https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
            default_model=settings.openrouter_model or "anthropic/claude-sonnet-4",
        )


class GroqProvider(AIProvider):
    def __init__(self):
        self._api_key = settings.groq_api_key
        self._default_model = settings.groq_model or "qwen/qwen3.8-27b"

    def chat(self, messages, *, model="", temperature=0.7, max_tokens=4096, response_format=None):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        body = {"model": model or self._default_model, "messages": messages,
                "temperature": temperature, "max_tokens": max_tokens}
        if response_format:
            body["response_format"] = response_format
        resp = requests.post(url, headers=headers, json=body, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


_PROVIDERS: dict[str, AIProvider] = {}


def get_provider(name: str) -> AIProvider:
    name = name.lower().strip()
    if name not in _PROVIDERS:
        if name == "deepseek":
            _PROVIDERS[name] = DeepSeekProvider()
        elif name == "openrouter":
            _PROVIDERS[name] = OpenRouterProvider()
        elif name == "groq":
            _PROVIDERS[name] = GroqProvider()
        else:
            raise ValueError(f"Unknown provider '{name}'. Use: deepseek, openrouter, groq")
    return _PROVIDERS[name]


def chat_with_fallback(messages, *, providers, model_overrides=None,
                       temperature=0.7, max_tokens=4096, response_format=None):
    """Try providers in order. Returns (provider_name, text)."""
    model_overrides = model_overrides or {}
    last_error = None
    for prov_name in providers:
        try:
            provider = get_provider(prov_name)
            model = model_overrides.get(prov_name, "")
            text = provider.chat(messages, model=model, temperature=temperature,
                                 max_tokens=max_tokens, response_format=response_format)
            return prov_name, text
        except Exception as exc:
            log.warning("Provider %s failed: %s", prov_name, exc)
            last_error = exc
    raise RuntimeError(f"All providers failed. Last error: {last_error}")
