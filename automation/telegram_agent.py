import os
import sys
import json
import urllib.request
from typing import Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TelegramAgent:
    """
    Telegram Agent (automation/telegram_agent.py)
    Dominio: Conector de comunicación entre la colmena de agentes y el CEO vía Telegram Bot API.
    Sostiene la notificación en tiempo real de eventos, alertas del sistema y métricas contables.
    """
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "mock_telegram_token")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "mock_chat_id")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text: str, target_chat_id: str = None) -> Dict[str, Any]:
        """Envía un mensaje formateado con Markdown a un Chat ID o al canal del CEO."""
        chat_id = target_chat_id or self.chat_id
        
        # Modo de prueba simulado si no se ha configurado un Token real en .env
        if "mock" in self.bot_token or not self.bot_token:
            print(f"📲 [TelegramAgent - Mock Mode] Para Chat ID {chat_id}:\n{text}\n")
            return {"status": "SUCCESS_MOCK", "recipient": chat_id}

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode())
                print(f"✅ [TelegramAgent] Mensaje entregado a Telegram.")
                return res
        except Exception as e:
            print(f"❌ [TelegramAgent] Error al enviar mensaje: {e}")
            return {"status": "ERROR", "details": str(e)}

    def notify_ceo_event(self, title: str, details: str) -> Dict[str, Any]:
        """Envía notificaciones operativas directamente al CEO."""
        msg = f"🔔 *[CYBERNICHE-LAB HQ]*\n\n📌 *{title}*\n{details}"
        return self.send_message(msg)

if __name__ == "__main__":
    agent = TelegramAgent()
    agent.notify_ceo_event("Módulo Integrado", "El TelegramAgent ha sido compilado y conectado correctamente a la colmena.")