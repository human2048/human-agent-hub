import os
from telegram import Bot

async def send_telegram_document(bot_token: str, chat_id: str, file_path: str, caption: str = ""):
    """
    Skill para enviar documentos (PDF, DOCX) directamente a Telegram.
    $0 Inversión - Usa API nativa de Telegram.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
        
    bot = Bot(token=bot_token)
    with open(file_path, 'rb') as doc:
        await bot.send_document(
            chat_id=chat_id,
            document=doc,
            caption=caption,
            parse_mode="Markdown"
        )