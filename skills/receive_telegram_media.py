from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

# Carpeta para guardar entradas recibidas
INPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "inputs"
INPUT_DIR.mkdir(parents=True, exist_ok=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga notas de voz enviadas por el usuario."""
    voice = update.message.voice
    file_id = voice.file_id
    new_file = await context.bot.get_file(file_id)
    
    file_path = INPUT_DIR / f"audio_{file_id[:8]}.ogg"
    await new_file.download_to_drive(file_path)
    
    await update.message.reply_text(f"🎙️ Audio recibido y guardado para procesamiento: `{file_path.name}`", parse_mode="Markdown")
    print(f"--> [InputSkill] Audio guardado en: {file_path}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga documentos o imágenes enviadas por el usuario."""
    doc = update.message.document
    file_id = doc.file_id
    file_name = doc.file_name or f"doc_{file_id[:8]}"
    
    new_file = await context.bot.get_file(file_id)
    file_path = INPUT_DIR / file_name
    await new_file.download_to_drive(file_path)
    
    await update.message.reply_text(f"📄 Documento recibido: `{file_name}`", parse_mode="Markdown")
    print(f"--> [InputSkill] Documento guardado en: {file_path}")