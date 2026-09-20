import asyncio
from skills.send_telegram_media import send_telegram_document

# Configuración con variables
BOT_TOKEN = "TU_BOT_TOKEN_AQUI"
CHAT_ID = "TU_CHAT_ID_AQUI"

async def run_pipeline():
    # Tu lógica actual de ejecución (FinancialAgent)
    # ...
    
    # Ruta del archivo generado por el agente
    report_file = "./reporte_financiero.docx"
    
    print("--> [TelegramAgent] Enviando reporte real a Telegram...")
    await send_telegram_document(
        bot_token="8810958085:AAH_a8jbTwsmNG4qsGZxutxWtMJCDJ6lOkA",
        chat_id="8552587368",
        file_path=report_file,
        caption="📊 *Reporte Financiero Ejecutado Con Éxito*"
    )

if __name__ == "__main__":
    asyncio.run(run_pipeline())