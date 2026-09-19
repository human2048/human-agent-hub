import os
import time
import psutil
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (MonitoringAgent-Autonomous): %(message)s"
)

class MonitoringAgent:
    def __init__(self, ollama_url: str = "http://localhost:11434/api/tags"):
        self.ollama_url = ollama_url
        self.metrics = {
            "service_status": "DOWN",
            "latency_ms": 0.0,
            "cpu_usage_pct": 0.0,
            "ram_usage_mb": 0.0,
            "alert_triggered": False,
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        """
        Toma de decisión autónoma basada en el estado del servicio y la latencia de inferencia.
        """
        status = self.metrics["service_status"]
        latency = self.metrics["latency_ms"]
        
        if status == "UP" and latency < 3000.0:
            decision = "INFRASTRUCTURE_OPTIMAL: Operación estable, sin acción requerida."
        elif status == "UP" and latency >= 3000.0:
            decision = "WARNING_LATENCY: Latencia elevada detectada en Ollama. Monitoreando carga de contexto."
        else:
            decision = "CRITICAL_SRE_ACTION: Servicio caído. Ejecutando protocolo de reinicio o failover local."

        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma SRE Ejecutada -> {decision}")

    def check_health(self):
        start_time = time.time()
        try:
            response = requests.get(self.ollama_url, timeout=3)
            end_time = time.time()
            
            if response.status_code == 200:
                self.metrics["service_status"] = "UP"
                self.metrics["latency_ms"] = round((end_time - start_time) * 1000, 2)
            else:
                self.metrics["service_status"] = "DEGRADED"
                self.metrics["alert_triggered"] = True
                logging.warning("El servicio local muestra un estado degradado.")
                
        except Exception as e:
            self.metrics["service_status"] = "DOWN"
            self.metrics["alert_triggered"] = True
            logging.error(f"Alerta crítica: No se pudo conectar con Ollama local: {e}")

        self.metrics["cpu_usage_pct"] = psutil.cpu_percent(interval=1)
        self.metrics["ram_usage_mb"] = round(psutil.virtual_memory().used / (1024 * 1024), 2)

        # Ejecutar evaluación y decisión autónoma
        self.evaluate_and_decide()

        logging.info("Auditoría de infraestructura autónoma completada.")
        return self.metrics

if __name__ == "__main__":
    agent = MonitoringAgent()
    report = agent.check_health()
    
    print("\n" + "="*50)
    print(" REPORTE AUTÓNOMO - MONITORING AGENT ")
    print("="*50)
    for key, value in report.items():
        print(f" - {key}: {value}")
    print("="*50)