import os
import sys
from typing import Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.financial_agent import FinancialAgent
from backend.cleaner_agent import CleanerAgent
from automation.lead_scraping_agent import LeadScrapingAgent
from frontend.code_quality_agent import FrontendBuilderAgent
from database.db_agent import DatabaseAgent

class OrchestratorAgent:
    """
    Orchestrator & Telegram Operations Agent (bot_listener.py)
    Rol: Director de Operaciones (COO) y Orquestador de la Colmena.
    Dominio: Coordinación síncrona de agentes ejecutores, gestión de comandos 
    del CEO y despacho de reportes ejecutivos.
    """
    def __init__(self):
        self.db = DatabaseAgent()
        self.financial = FinancialAgent()
        self.cleaner = CleanerAgent()
        self.scraper = LeadScrapingAgent()
        self.frontend = FrontendBuilderAgent()

    def process_command(self, command: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Interpreta el comando ejecutivo del CEO, delega en la fuerza laboral 
        y centraliza el resultado para el despacho en Telegram.
        """
        payload = payload or {}
        cmd = command.lower().strip()
        
        print(f"🤖 [OrchestratorCOO] Procesando directiva ejecutiva: '{cmd}'")

        try:
            if "financ" in cmd or "mrr" in cmd:
                result = self.financial.execute(
                    mrr_price=payload.get("mrr_price", 29.0),
                    active_subscribers=payload.get("subscribers", 1),
                    acquisition_cost=payload.get("cac", 10.0)
                )
                return {"status": "SUCCESS", "agent": "FinancialAgent", "data": result}

            elif "scrap" in cmd or "lead" in cmd:
                category = payload.get("category", "Restaurantes")
                result = self.scraper.execute(category=category)
                return {"status": "SUCCESS", "agent": "LeadScrapingAgent", "data": result}

            elif "frontend" in cmd or "web" in cmd or "landing" in cmd:
                brand = payload.get("brand_name", "Micro-SaaS Local")
                result = self.frontend.execute(brand_name=brand)
                return {"status": "SUCCESS", "agent": "FrontendBuilderAgent", "data": result}

            elif "clean" in cmd or "sanear" in cmd:
                raw = payload.get("raw_data", [{"item": "muestra", "price": "10.00"}])
                result = self.cleaner.execute(raw_data=raw)
                return {"status": "SUCCESS", "agent": "CleanerAgent", "data": result}

            else:
                return {
                    "status": "UNKNOWN_COMMAND",
                    "message": f"Directiva '{command}' no reconocida por la colmena operativa."
                }

        except Exception as e:
            print(f"❌ [OrchestratorCOO] Error crítico ejecutando directiva: {e}")
            return {"status": "ERROR", "error_message": str(e)}

if __name__ == "__main__":
    coordinator = OrchestratorAgent()
    # Simulación de orden ejecutiva del CEO
    coordinator.process_command("frontend", {"brand_name": "Mi Micro-SaaS Élite"})
    coordinator.process_command("financial", {"subscribers": 5, "mrr_price": 49.0})