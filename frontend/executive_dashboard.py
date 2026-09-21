import json
from pathlib import Path

from database.db_agent import DatabaseAgent
from backend.financial_agent import FinancialAgent


DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "cyberniche.db"


class ExecutiveDashboard:
    """
    Dashboard Ejecutivo SaaS (executive_dashboard.py)
    Consolida la métrica financiera en tiempo real consultando
    la BD Multi-Tenant y el FinancialAgent.
    """
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db = DatabaseAgent(db_path=db_path)
        self.financial_agent = FinancialAgent(monthly_fee=29.00)

    def render_dashboard_data(self) -> dict:
        """Extrae el estado actual del negocio para consumir en Frontend o CLI."""
        # 1. Total de clientes y estado
        tenants = self.db.execute_query("SELECT id, business_name, is_active, created_at FROM tenants;")
        active_tenants = [t for t in tenants if t[2] == 1]
        
        # 2. Total cobrado en Setup Fees e Ingresos Recurrentes
        payments = self.db.execute_query("SELECT transaction_type, amount FROM payment_transactions WHERE status = 'APPROVED';")
        
        total_setup_fees = sum(p[1] for p in payments if p[0] == "SETUP_FEE")
        total_subscription_revenue = sum(p[1] for p in payments if p[0] == "RECURRING_SUBSCRIPTION")
        
        # 3. Métricas Financieras proyectadas
        financial_report = self.financial_agent.calculate_saas_metrics(
            active_tenants=len(active_tenants),
            canceled_tenants=0
        )
        
        cash_projection = self.financial_agent.project_cash_flow(
            current_mrr=financial_report["metrics"]["monthly_recurrent_revenue_mrr"],
            setup_fees_collected=total_setup_fees,
            fixed_costs=0.0,
            months=6
        )

        return {
            "business_summary": {
                "total_tenants": len(tenants),
                "active_tenants": len(active_tenants),
                "total_setup_fees_usd": round(total_setup_fees, 2),
                "total_subscription_revenue_usd": round(total_subscription_revenue, 2),
                "total_gross_revenue_usd": round(total_setup_fees + total_subscription_revenue, 2)
            },
            "saas_kpis": financial_report["metrics"],
            "6_month_cash_projection": cash_projection["cash_flow_projection"]
        }

if __name__ == "__main__":
    dash = ExecutiveDashboard()
    print("📈 DASHBOARD EJECUTIVO - CYBERNICHE-LAB")
    print(json.dumps(dash.render_dashboard_data(), indent=2, ensure_ascii=False))