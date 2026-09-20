import asyncio
from skills.generate_report import create_docx_report, create_pdf_report
from skills.send_telegram_media import send_telegram_document

BOT_TOKEN = "8810958085:AAH_a8jbTwsmNG4qsGZxutxWtMJCDJ6lOkA"
CHAT_ID = "123456789"  # Reemplazar con tu ID numérico de @userinfobot

async def run_pipeline():
    print("--> [Agent] Generando contenido del informe...")
    
    titulo = "Reporte Ejecutivo de Rendimiento SaaS"
    contenido = [
        "Estado del Pipeline: OPERATIVO",
        "MRR Actual: $29.0 USD | ARR Estimado: $348.0 USD",
        "Tasa de Churn: 0.0%",
        "Este informe fue generado de manera autónoma por la colmena de agentes de CyberNiche Lab."
    ]
    
    # 1. Generar archivo PDF
    pdf_path = create_pdf_report(titulo, contenido, "reporte_ejecutivo.pdf")
    print(f"--> [Skill] PDF generado en {pdf_path}")
    
    # 2. Enviar a Telegram
    print("--> [TelegramAgent] Enviando documento PDF a Telegram...")
    await send_telegram_document(
        bot_token="8810958085:AAH_a8jbTwsmNG4qsGZxutxWtMJCDJ6lOkA",
        chat_id="8552587368",
        file_path=pdf_path,
        caption="📄 *Reporte PDF Automático Generado por la Colmena*"
    )

if __name__ == "__main__":
    asyncio.run(run_pipeline())