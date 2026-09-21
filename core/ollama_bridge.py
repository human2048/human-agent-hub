"""Asynchronous bridge between validated Telegram text and Ollama."""

from __future__ import annotations

import logging
from typing import Any

import httpx

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:latest"
OLLAMA_TIMEOUT_SECONDS = 45.0

logger = logging.getLogger(__name__)


class OllamaBridgeError(RuntimeError):
    """Base error raised when Ollama cannot produce a response."""


class OllamaTimeoutError(OllamaBridgeError):
    """Raised when Ollama does not respond within the configured timeout."""


class OllamaConnectionError(OllamaBridgeError):
    """Raised when the local Ollama service cannot be reached."""


class OllamaResponseError(OllamaBridgeError):
    """Raised when Ollama returns an invalid or unsuccessful response."""


def _validate_text(validated_text: str) -> str:
    if not isinstance(validated_text, str):
        raise TypeError("validated_text debe ser una cadena de texto.")

    text = validated_text.strip()
    if not text:
        raise ValueError("validated_text no puede estar vacío.")

    return text


async def generate_response(
    validated_text: str, *, timeout: float = OLLAMA_TIMEOUT_SECONDS
) -> str:
    """Generate a response from Ollama for already validated Telegram text.

    The request is non-streaming and has a bounded timeout so callers
    can await it from Telegram's async handler without blocking the event loop.

    Raises:
        TypeError: If ``validated_text`` is not a string.
        ValueError: If ``validated_text`` is empty after trimming.
        OllamaTimeoutError: If Ollama exceeds the request timeout.
        OllamaConnectionError: If the local service cannot be reached.
        OllamaResponseError: If Ollama returns an HTTP or payload error.
    """
    prompt = _validate_text(validated_text)
    payload: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(OLLAMA_GENERATE_URL, json=payload)
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        logger.warning("Ollama excedió el timeout de %s segundos.", timeout)
        raise OllamaTimeoutError(
            f"Ollama no respondió en {timeout} segundos."
        ) from exc
    except httpx.RequestError as exc:
        logger.error("No se pudo conectar con Ollama en %s: %s", OLLAMA_GENERATE_URL, exc)
        raise OllamaConnectionError(
            "No se pudo conectar con el servicio local de Ollama."
        ) from exc
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Ollama devolvió HTTP %s: %s",
            exc.response.status_code,
            exc.response.text[:500],
        )
        raise OllamaResponseError(
            f"Ollama devolvió un error HTTP {exc.response.status_code}."
        ) from exc

    try:
        result = response.json()
    except ValueError as exc:
        raise OllamaResponseError("Ollama devolvió una respuesta JSON inválida.") from exc

    if not isinstance(result, dict) or not isinstance(result.get("response"), str):
        raise OllamaResponseError(
            "La respuesta de Ollama no contiene el campo de texto 'response'."
        )

    return result["response"]


__all__ = [
    "OLLAMA_GENERATE_URL",
    "OLLAMA_MODEL",
    "OLLAMA_TIMEOUT_SECONDS",
    "OllamaBridgeError",
    "OllamaConnectionError",
    "OllamaResponseError",
    "OllamaTimeoutError",
    "generate_response",
]
