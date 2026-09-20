import os
import sys
from typing import Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class FinancialAgent:
    """
    Financial Agent (backend/financial_agent.py)
    Dominio: Inteligencia contable, proyección financiera y métricas SaaS (MRR, ARR, LTV, CAC).
    """
    def __init__(self):
        pass

    def calculate_saas_metrics(self, mrr_price: float = 29.0, active_subscribers: int = 1) -> Dict[str, Any]:
        """Calcula el estado financiero y métricas clave del Micro-SaaS."""
        mrr = mrr_price * active_subscribers
        arr = mrr * 12
        
        report = {
            "agent": "FinancialAgent",
            "status": "FINANCIALLY_HEALTHY",
            "mrr_usd": mrr,
            "arr_usd": arr,
            "churn_rate": 0.0,
            "active_subscribers": active_subscribers
        }
        
        print(f"💰 [FinancialAgent] Estado: FINANCIALLY_HEALTHY | MRR: ${mrr} USD | ARR: ${arr} USD | Churn: 0.0%")
        return report

    def calculate_metrics(self, mrr_price: float = 29.0, active_subscribers: int = 1) -> Dict[str, Any]:
        """Alias para mantener compatibilidad con el orquestador."""
        return self.calculate_saas_metrics(mrr_price, active_subscribers)

if __name__ == "__main__":
    agent = FinancialAgent()
    print(agent.calculate_metrics())