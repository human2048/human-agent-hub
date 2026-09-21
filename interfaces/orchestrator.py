import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from skills.generate_report import create_pdf_report
from skills.send_telegram_media import send_telegram_document
from database.db_agent import SANDBOX_ROOT, validate_sandbox_path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")


def validate_telegram_configuration() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en el archivo .env.")
    if not OWNER_ID:
        raise RuntimeError("Falta OWNER_ID en el archivo .env.")

async def run_pipeline():
    validate_telegram_configuration()
    print("--> [Agent] Generando contenido del informe...")
    
    titulo = "Reporte Ejecutivo de Rendimiento SaaS"
    contenido = [
        "Estado del Pipeline: OPERATIVO",
        "MRR Actual: $29.0 USD | ARR Estimado: $348.0 USD",
        "Tasa de Churn: 0.0%",
        "Este informe fue generado de manera autónoma por la colmena de agentes de CyberNiche Lab."
    ]
    
    # 1. Generar archivo PDF
    pdf_path = validate_sandbox_path(SANDBOX_ROOT / "reporte_ejecutivo.pdf")
    pdf_path = create_pdf_report(titulo, contenido, str(pdf_path))
    print(f"--> [Skill] PDF generado en {pdf_path}")
    
    # 2. Enviar a Telegram
    print("--> [TelegramAgent] Enviando documento PDF a Telegram...")
    await send_telegram_document(
        bot_token=BOT_TOKEN,
        chat_id=OWNER_ID,
        file_path=pdf_path,
        caption="📄 *Reporte PDF Automático Generado por la Colmena*"
    )

if __name__ == "__main__":
    asyncio.run(run_pipeline())