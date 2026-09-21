import os
import sys
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, MessageHandler, filters

# Asegurar importación del directorio raíz al ejecutar este archivo directamente.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.financial_agent import FinancialAgent
from backend.cleaner_agent import CleanerAgent
from automation.lead_scraping_agent import LeadScrapingAgent
from frontend.code_quality_agent import FrontendBuilderAgent
from database.db_agent import DatabaseAgent, SANDBOX_ROOT, validate_sandbox_path
from core.ollama_bridge import OllamaBridgeError, generate_response

load_dotenv(PROJECT_ROOT / ".env")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")


def validate_telegram_configuration() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en el archivo .env.")
    if not OWNER_ID:
        raise RuntimeError("Falta OWNER_ID en el archivo .env.")


def is_authorized(update: Update) -> bool:
    user = update.effective_user
    return bool(user and OWNER_ID and str(user.id) == OWNER_ID.strip())

class OrchestratorAgent:
    """
    Orchestrator & Telegram Operations Agent (bot_listener.py)
    Rol: Director de Operaciones (COO) y Orquestador de la Colmena.
    Dominio: Coordinación síncrona de agentes ejecutores, gestión de comandos 
    del CEO y despacho de reportes ejecutivos.
    """
    def __init__(self):
        self.db = DatabaseAgent()
        self.financial = FinancialAgent()
        self.cleaner = CleanerAgent()
        self.scraper = LeadScrapingAgent()
        self.frontend = FrontendBuilderAgent(frontend_dir=SANDBOX_ROOT)
        self.db.execute_transaction(
            """
            CREATE TABLE IF NOT EXISTS agent_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                command TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                response TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def _record_interaction(self, user_id: str, command: str, reasoning: str,
                            response: str, status: str) -> None:
        self.db.execute_transaction(
            """
            INSERT INTO agent_interactions
                (user_id, command, reasoning, response, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, command, reasoning, response, status),
        )

    def process_command(self, command: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Interpreta el comando ejecutivo del CEO, delega en la fuerza laboral 
        y centraliza el resultado para el despacho en Telegram.
        """
        payload = payload or {}
        cmd = command.lower().strip()
        
        print(f"🤖 [OrchestratorCOO] Procesando directiva ejecutiva: '{cmd}'")

        try:
            if "financ" in cmd or "mrr" in cmd:
                result = self.financial.execute(
                    mrr_price=payload.get("mrr_price", 29.0),
                    active_subscribers=payload.get("subscribers", 1),
                    acquisition_cost=payload.get("cac", 10.0)
                )
                return {"status": "SUCCESS", "agent": "FinancialAgent", "data": result}

            elif "scrap" in cmd or "lead" in cmd:
                category = payload.get("category", "Restaurantes")
                result = self.scraper.execute(category=category)
                return {"status": "SUCCESS", "agent": "LeadScrapingAgent", "data": result}

            elif "frontend" in cmd or "web" in cmd or "landing" in cmd:
                brand = payload.get("brand_name", "Micro-SaaS Local")
                file_name = str(payload.get("file_name", "generated_interface.html"))
                validate_sandbox_path(SANDBOX_ROOT / file_name)
                result = self.frontend.execute(file_name=file_name, brand_name=brand)
                return {"status": "SUCCESS", "agent": "FrontendBuilderAgent", "data": result}

            elif "clean" in cmd or "sanear" in cmd:
                raw = payload.get("raw_data", [{"item": "muestra", "price": "10.00"}])
                result = self.cleaner.execute(raw_data=raw)
                return {"status": "SUCCESS", "agent": "CleanerAgent", "data": result}

            else:
                return {
                    "status": "UNKNOWN_COMMAND",
                    "message": f"Directiva '{command}' no reconocida por la colmena operativa."
                }

        except Exception as e:
            print(f"❌ [OrchestratorCOO] Error crítico ejecutando directiva: {e}")
            return {"status": "ERROR", "error_message": str(e)}

    async def process_telegram_message(self, user_id: str, message: str) -> str:
        """Route an authorized Telegram message through Ollama and persist it."""
        command = message.strip()
        try:
            response = await generate_response(command)
            self._record_interaction(
                user_id, command,
                "Inferencia local solicitada y completada por Ollama.",
                response, "SUCCESS",
            )
            return response
        except (OllamaBridgeError, TypeError, ValueError) as exc:
            error_message = f"Error interno: No se pudo conectar con el motor local ({exc})"
            self._record_interaction(
                user_id, command,
                "La inferencia local falló o agotó el tiempo de espera.",
                error_message, "ERROR",
            )
            return error_message


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        return
    if not update.message or not update.message.text or not update.effective_user:
        return
    coordinator = context.application.bot_data["orchestrator"]
    response = await coordinator.process_telegram_message(
        str(update.effective_user.id), update.message.text
    )
    await update.message.reply_text(response)


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"❌ [TelegramListener] Error recuperable: {context.error}")


def create_application() -> Application:
    validate_telegram_configuration()
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.bot_data["orchestrator"] = OrchestratorAgent()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(handle_error)
    return application


def run_bot() -> None:
    create_application().run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    run_bot()