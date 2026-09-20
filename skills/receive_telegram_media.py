import os
from telegram import Update
from telegram.ext import ContextTypes

# Carpeta para guardar entradas recibidas
INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "inputs")
os.makedirs(INPUT_DIR, exist_ok=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga notas de voz enviadas por el usuario."""
    voice = update.message.voice
    file_id = voice.file_id
    new_file = await context.bot.get_file(file_id)
    
    file_path = os.path.join(INPUT_DIR, f"audio_{file_id[:8]}.ogg")
    await new_file.download_to_drive(file_path)
    
    await update.message.reply_text(f"🎙️ Audio recibido y guardado para procesamiento: `{os.path.basename(file_path)}`", parse_mode="Markdown")
    print(f"--> [InputSkill] Audio guardado en: {file_path}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga documentos o imágenes enviadas por el usuario."""
    doc = update.message.document
    file_id = doc.file_id
    file_name = doc.file_name or f"doc_{file_id[:8]}"
    
    new_file = await context.bot.get_file(file_id)
    file_path = os.path.join(INPUT_DIR, file_name)
    await new_file.download_to_drive(file_path)
    
    await update.message.reply_text(f"📄 Documento recibido: `{file_name}`", parse_mode="Markdown")
    print(f"--> [InputSkill] Documento guardado en: {file_path}")