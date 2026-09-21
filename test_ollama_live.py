"""Live transactional smoke test for the local Ollama bridge."""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone
from uuid import uuid4

import httpx
from core.ollama_bridge import (
    OLLAMA_GENERATE_URL,
    OLLAMA_MODEL,
    OllamaBridgeError,
    OllamaTimeoutError,
    generate_response,
)
from database.db_agent import DatabaseAgent

PROMPT = "Escribe una función corta en Python para validar un JSON."
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
INFERENCE_TIMEOUT_SECONDS = 90.0
MAX_ATTEMPTS = 2


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_test_table(database: DatabaseAgent) -> None:
    database.execute_transaction(
        """
        CREATE TABLE IF NOT EXISTS ollama_test_sessions (
            session_id TEXT PRIMARY KEY,
            prompt TEXT NOT NULL,
            response TEXT,
            status TEXT NOT NULL,
            latency_ms REAL,
            endpoint TEXT NOT NULL,
            model TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT NOT NULL
        )
        """
    )


async def warm_up_ollama() -> None:
    """Touch Ollama's model catalog before the inference request."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(OLLAMA_TAGS_URL)
        response.raise_for_status()


async def run_live_test() -> dict[str, object]:
    """Call Ollama asynchronously and persist the complete test transaction."""
    database = DatabaseAgent()
    ensure_test_table(database)
    session_id = str(uuid4())
    started_at = utc_now()
    response_text: str | None = None
    status = "FALLO"
    error_message: str | None = None
    attempts = 0
    started_clock = time.perf_counter()

    try:
        await warm_up_ollama()
        for attempts in range(1, MAX_ATTEMPTS + 1):
            try:
                inference_task = asyncio.create_task(
                    generate_response(PROMPT, timeout=INFERENCE_TIMEOUT_SECONDS)
                )
                await asyncio.sleep(0)
                response_text = await inference_task
                status = "EXITO"
                break
            except OllamaTimeoutError as exc:
                error_message = (
                    f"Intento {attempts}/{MAX_ATTEMPTS} agotó el timeout: {exc}"
                )
                if attempts == MAX_ATTEMPTS:
                    break
                print(f"⚠️ [Ollama] {error_message}. Reintentando...")
    except (OllamaBridgeError, TypeError, ValueError) as exc:
        error_message = str(exc)
    except Exception as exc:
        error_message = f"Error inesperado: {exc}"
    finally:
        latency_ms = round((time.perf_counter() - started_clock) * 1000, 3)
        database.execute_transaction(
            """
            INSERT INTO ollama_test_sessions
                (session_id, prompt, response, status, latency_ms,
                 endpoint, model, started_at, finished_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                PROMPT,
                response_text if response_text is not None else error_message,
                status,
                latency_ms,
                OLLAMA_GENERATE_URL,
                OLLAMA_MODEL,
                started_at,
                utc_now(),
            ),
        )

    return {
        "session_id": session_id,
        "status": status,
        "prompt": PROMPT,
        "response": response_text,
        "error": error_message,
        "latency_ms": latency_ms,
        "endpoint": OLLAMA_GENERATE_URL,
        "model": OLLAMA_MODEL,
        "attempts": attempts,
        "timeout_seconds": INFERENCE_TIMEOUT_SECONDS,
        "warm_up_endpoint": OLLAMA_TAGS_URL,
        "database": str(database.db_path),
    }


def main() -> int:
    result = asyncio.run(run_live_test())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "EXITO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
