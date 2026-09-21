from datetime import datetime, timezone
from pathlib import Path
import time
from uuid import uuid4

from dotenv import load_dotenv

from core.ollama_bridge import (
    OLLAMA_GENERATE_URL,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT_SECONDS,
)
from database.db_agent import DatabaseAgent, SANDBOX_ROOT
from interfaces.bot_listener import create_application, validate_telegram_configuration


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")
POLL_RETRY_BASE_SECONDS = 5
POLL_RETRY_MAX_SECONDS = 60


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def initialize_runtime() -> tuple[DatabaseAgent, str]:
    """Validate runtime dependencies and persist the beginning of a session."""
    validate_telegram_configuration()
    if not OLLAMA_GENERATE_URL.startswith("http://localhost:11434/"):
        raise RuntimeError("El puente Ollama no apunta al servicio local esperado.")
    if OLLAMA_MODEL != "qwen2.5-coder:latest":
        raise RuntimeError("El modelo Ollama configurado no es el esperado.")
    if OLLAMA_TIMEOUT_SECONDS <= 0:
        raise RuntimeError("El timeout de Ollama debe ser mayor que cero.")

    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)
    database = DatabaseAgent()
    journal_mode = database.execute_query("PRAGMA journal_mode;")
    if not journal_mode or str(journal_mode[0][0]).lower() != "wal":
        raise RuntimeError("data/cyberniche.db no está funcionando en modo WAL.")

    database.execute_transaction(
        """
        CREATE TABLE IF NOT EXISTS runtime_sessions (
            session_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            ollama_url TEXT NOT NULL,
            ollama_model TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT
        )
        """
    )
    session_id = str(uuid4())
    database.execute_transaction(
        """
        INSERT INTO runtime_sessions
            (session_id, status, ollama_url, ollama_model, started_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (session_id, "STARTING", OLLAMA_GENERATE_URL, OLLAMA_MODEL, _utc_now()),
    )
    return database, session_id


def update_session(database: DatabaseAgent, session_id: str, status: str) -> None:
    if status == "RUNNING":
        database.execute_transaction(
            "UPDATE runtime_sessions SET status = ?, finished_at = NULL WHERE session_id = ?",
            (status, session_id),
        )
        return

    database.execute_transaction(
        "UPDATE runtime_sessions SET status = ?, finished_at = ? WHERE session_id = ?",
        (status, _utc_now(), session_id),
    )


def run_polling_loop(database: DatabaseAgent, session_id: str) -> None:
    """Keep Telegram long-polling alive across temporary network failures."""
    retry_count = 0
    while True:
        try:
            update_session(database, session_id, "RUNNING")
            application = create_application()
            application.run_polling(drop_pending_updates=True)
            update_session(database, session_id, "STOPPED")
            return
        except KeyboardInterrupt:
            update_session(database, session_id, "STOPPED")
            raise
        except Exception as exc:
            retry_count += 1
            delay = min(
                POLL_RETRY_BASE_SECONDS * (2 ** (retry_count - 1)),
                POLL_RETRY_MAX_SECONDS,
            )
            update_session(database, session_id, "RETRYING")
            print(
                f"⚠️ [HiveRunner] Polling interrumpido ({exc}). "
                f"Reintento {retry_count} en {delay}s."
            )
            time.sleep(delay)

def main():
    print("🚀 [HiveRunner] Validando base de datos, sandbox y configuración...")
    database, session_id = initialize_runtime()
    try:
        print(
            f"✅ [HiveRunner] WAL activo. Sandbox listo. Ollama: {OLLAMA_MODEL} "
            f"({OLLAMA_TIMEOUT_SECONDS}s timeout)."
        )
        run_polling_loop(database, session_id)
    except KeyboardInterrupt:
        update_session(database, session_id, "STOPPED")
        print("🛑 [HiveRunner] Polling detenido por el operador.")
    except Exception:
        update_session(database, session_id, "FAILED")
        raise
    else:
        update_session(database, session_id, "STOPPED")

if __name__ == "__main__":
    main()