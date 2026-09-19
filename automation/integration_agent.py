import os
import time
import requests
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (IntegrationAgent-Autonomous): %(message)s"
)

class IntegrationAgent:
    def __init__(self, webhook_target_url: str = "https://httpbin.org/post"):
        self.webhook_target_url = webhook_target_url
        self.metrics = {
            "events_dispatched": 0,
            "webhook_success_rate": 0.0,
            "integration_latency_ms": 0.0,
            "payload_integrity_score": 100.0,
            "errors_handled": 0,
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        """
        Toma de decisión autónoma basada en el éxito del webhook, latencia e integridad del payload.
        """
        success_rate = self.metrics["webhook_success_rate"]
        latency = self.metrics["integration_latency_ms"]
        integrity = self.metrics["payload_integrity_score"]

        if success_rate == 100.0 and integrity == 100.0 and latency < 3000.0:
            decision = "INTEGRATION_OPTIMAL: Webhooks despachados y sincronizados correctamente."
        elif success_rate == 100.0 and latency >= 3000.0:
            decision = "WARNING_HIGH_LATENCY: Integración lenta pero exitosa. Monitorear endpoints externos."
        else:
            decision = "CRITICAL_INTEGRATION_FAILURE: Fallo en entrega de webhook o payload corrupto. Activar cola de reintentos."

        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma de Integration Ejecutada -> {decision}")

    def trigger_workflow_event(self, event_payload: dict):
        start_time = time.time()
        success_count = 0
        total_events = 1

        self.metrics["events_dispatched"] = total_events

        try:
            logging.info(f"Despachando evento automatizado autónomo hacia: {self.webhook_target_url}")
            
            if not isinstance(event_payload, dict) or not event_payload:
                self.metrics["payload_integrity_score"] = 0.0
                self.metrics["errors_handled"] += 1
                self.metrics["autonomous_decision"] = "CRITICAL_INVALID_PAYLOAD"
                logging.error("Error de integridad: Payload inválido o vacío.")
                return None

            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.webhook_target_url, 
                data=json.dumps(event_payload), 
                headers=headers, 
                timeout=5
            )
            
            end_time = time.time()
            self.metrics["integration_latency_ms"] = round((end_time - start_time) * 1000, 2)

            if response.status_code == 200:
                success_count += 1
                self.metrics["webhook_success_rate"] = 100.0
                logging.info("Evento procesado y entregado exitosamente.")
            else:
                self.metrics["webhook_success_rate"] = 0.0
                self.metrics["errors_handled"] += 1
                logging.warning(f"Endpoint respondió con código no exitoso: {response.status_code}")

            # Ejecutar evaluación y decisión autónoma
            self.evaluate_and_decide()

            return self.metrics

        except Exception as e:
            self.metrics["errors_handled"] += 1
            self.metrics["webhook_success_rate"] = 0.0
            self.metrics["autonomous_decision"] = "CRITICAL_EXCEPTION"
            logging.error(f"Excepción crítica disparando evento de integración: {e}")
            return None

if __name__ == "__main__":
    sample_event = {
        "event_type": "USER_REGISTERED_AUTONOMOUS",
        "user_email": "test_user@cyberniche.lab",
        "timestamp": time.time()
    }

    agent = IntegrationAgent()
    report = agent.trigger_workflow_event(sample_event)

    if report:
        print("\n" + "="*50)
        print(" REPORTE AUTÓNOMO - INTEGRATION AGENT ")
        print("="*50)
        for key, value in report.items():
            print(f" - {key}: {value}")
        print("="*50)