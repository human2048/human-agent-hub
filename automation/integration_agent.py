import os
import sys
import time
from typing import Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class IntegrationAgent:
    """
    Integration Agent (automation/integration_agent.py)
    Dominio: Integraciones de pasarelas de pago y despacho de webhooks (ePayco, Wompi, Stripe).
    """
    def __init__(self):
        pass

    def process_payment_webhook(self, tenant_id: str, amount: float) -> Dict[str, Any]:
        """Procesa y valida la confirmación de pago entrante."""
        event = {
            "agent": "IntegrationAgent",
            "event": "PAYMENT_RECEIVED",
            "tenant_id": tenant_id,
            "amount": amount,
            "currency": "USD",
            "timestamp": time.time(),
            "status": "APPROVED"
        }
        print(f"💳 [IntegrationAgent] Webhook procesado exitosamente para '{tenant_id}' por ${amount} USD.")
        return event

    def simulate_payment_webhook(self, tenant_id: str, amount: float) -> Dict[str, Any]:
        """Alias para mantener compatibilidad con el orquestador."""
        return self.process_payment_webhook(tenant_id, amount)

if __name__ == "__main__":
    agent = IntegrationAgent()
    print(agent.simulate_payment_webhook("restaurant_demo", 50.0))