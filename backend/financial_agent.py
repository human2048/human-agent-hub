import os
import sys
from typing import Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class FinancialAgent:
    """
    Financial Agent (backend/financial_agent.py)
    Rol: Director Financiero (CFO) y Arquitecto de Métricas SaaS.
    Dominio: Inteligencia contable basada en benchmarks globales de la industria SaaS (MRR, ARR, LTV, CAC, Churn, Payback).
    """
    def __init__(self):
        pass

    def execute(self, mrr_price: float = 29.0, active_subscribers: int = 1, acquisition_cost: float = 15.0) -> Dict[str, Any]:
        """
        Calcula y audita las finanzas del Micro-SaaS aplicando modelos de rentabilidad 
        utilizados por fondos de inversión y startups de éxito en Silicon Valley.
        """
        try:
            if mrr_price < 0 or active_subscribers < 0 or acquisition_cost < 0:
                raise ValueError("Los parámetros financieros no pueden tener valores negativos.")

            # Modelado financiero avanzado de nivel SaaS
            mrr = float(mrr_price * active_subscribers)
            arr = float(mrr * 12)
            
            # Estándar global SaaS: Asumiendo un Churn mensual saludable del 5% y LTV estimado a 12 meses
            estimated_monthly_churn = 0.05
            arpu = mrr_price  # Average Revenue Per User
            ltv = float(arpu / estimated_monthly_churn) if estimated_monthly_churn > 0 else 0.0
            
            # Relación LTV / CAC (Un ratio superior a 3x indica un negocio altamente escalable)
            cac_ratio = float(ltv / acquisition_cost) if acquisition_cost > 0 else 0.0
            
            # Diagnóstico de salud financiera basado en datos
            if cac_ratio >= 3.0 and mrr > 0:
                health_status = "SCALABLE_HIGH_GROWTH"
                diagnostic = "El modelo financiero muestra una relación LTV/CAC óptima para inversión en escala."
            elif mrr > 0:
                health_status = "STABLE_EARLY_STAGE"
                diagnostic = "Operación sostenible en fase inicial. Se recomienda optimizar el costo de adquisición."
            else:
                health_status = "PRE_REVENUE"
                diagnostic = "Sin ingresos activos registrados en el periodo actual."

            report = {
                "agent": "FinancialAgent",
                "status": health_status,
                "mrr_usd": round(mrr, 2),
                "arr_usd": round(arr, 2),
                "estimated_ltv": round(ltv, 2),
                "estimated_cac": round(acquisition_cost, 2),
                "ltv_cac_ratio": round(cac_ratio, 2),
                "churn_rate_benchmark": estimated_monthly_churn * 100,
                "active_subscribers": active_subscribers,
                "strategic_insight": diagnostic
            }
            
            print(f"💰 [FinancialAgent CFO] Estado: {health_status} | MRR: ${mrr:,.2f} USD | ARR: ${arr:,.2f} USD | LTV/CAC: {cac_ratio:.1f}x")
            return report

        except Exception as e:
            print(f"❌ [FinancialAgent] Error crítico en análisis financiero: {e}")
            return {
                "agent": "FinancialAgent",
                "status": "ERROR",
                "error_message": str(e)
            }

if __name__ == "__main__":
    agent = FinancialAgent()
    agent.execute(mrr_price=29.0, active_subscribers=10, acquisition_cost=10.0)