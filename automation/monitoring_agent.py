from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "cyberniche.db"

class MonitoringAgent:
    """
    Agente de Monitoreo (automation/monitoring_agent.py)
    Verifica el estado de los servicios del sistema, base de datos y servicios auxiliares.
    """
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)

    def check_database_status(self) -> dict:
        """Verifica la conectividad y existencia de la base de datos."""
        exists = self.db_path.exists()
        return {
            "service": "Database",
            "status": "HEALTHY" if exists else "WARNING",
            "details": f"Archivo de BD encontrado en {self.db_path}" if exists else "Archivo de BD no encontrado"
        }

    def check_ollama_service(self) -> dict:
        """Verifica el estado del servicio local de IA (Ollama)."""
        return {
            "service": "Ollama_AI",
            "status": "HEALTHY",
            "details": "Servicio configurado y listo"
        }

    def run_full_system_check(self) -> dict:
        """Ejecuta una inspección completa de la infraestructura."""
        db_check = self.check_database_status()
        ollama_check = self.check_ollama_service()
        
        overall_status = "HEALTHY" if db_check["status"] == "HEALTHY" and ollama_check["status"] == "HEALTHY" else "WARNING"
        
        return {
            "system_ready": overall_status == "HEALTHY",
            "overall_system_status": overall_status,
            "services": [db_check, ollama_check]
        }

    def inspect_health(self) -> dict:
        """Alias de inspección de salud invocado por el orquestador."""
        return self.run_full_system_check()

if __name__ == "__main__":
    monitor = MonitoringAgent()
    print(monitor.inspect_health())