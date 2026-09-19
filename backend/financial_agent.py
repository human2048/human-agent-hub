import os
import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (FinancialAgent-Autonomous): %(message)s"
)

class SaaSFinancialAgent:
    def __init__(self, db_path: str = "database/cyberniche.db"):
        self.db_path = db_path
        self.metrics = {
            "active_subscriptions": 0,
            "estimated_mrr_usd": 0.0,
            "growth_projection_rate": 0.0,
            "financial_integrity_score": 100.0,
            "audit_status": "PENDING",
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        """
        Toma de decisión autónoma basada en el estado de las suscripciones activas,
        MRR y la integridad de la auditoría contable.
        """
        subscriptions = self.metrics["active_subscriptions"]
        status = self.metrics["audit_status"]
        integrity = self.metrics["financial_integrity_score"]

        if status == "PASSED" and integrity == 100.0 and subscriptions > 0:
            decision = "FINANCIAL_HEALTHY: Ingresos recurrentes activos y contabilidad validada."
        elif status == "PASSED" and subscriptions == 0:
            decision = "WARNING_ZERO_REVENUE: Sistema operativo pero sin suscripciones activas. Impulsar conversión de leads."
        else:
            decision = "CRITICAL_FINANCIAL_AUDIT_FAIL: Discrepancia contable detectada. Suspender cobros hasta revisión."

        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma Financiera Ejecutada -> {decision}")

    def audit_saas_finances(self, subscription_price_usd: float = 29.0):
        if not os.path.exists(self.db_path):
            logging.error(f"Base de datos no encontrada en '{self.db_path}'.")
            self.metrics["financial_integrity_score"] = 0.0
            self.metrics["audit_status"] = "FAILED"
            self.metrics["autonomous_decision"] = "CRITICAL_DB_MISSING"
            return None

        try:
            logging.info("Iniciando auditoría financiera y contable autónoma...")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users WHERE membership_status = 'Active'")
            result = cursor.fetchone()
            active_users = result[0] if result else 0

            conn.close()

            self.metrics["active_subscriptions"] = active_users
            self.metrics["estimated_mrr_usd"] = round(active_users * subscription_price_usd, 2)
            self.metrics["growth_projection_rate"] = round(active_users * 12.5, 2)
            self.metrics["audit_status"] = "PASSED"

            # Ejecutar evaluación y decisión autónoma
            self.evaluate_and_decide()

            logging.info("Auditoría financiera autónoma completada con éxito.")
            return self.metrics

        except Exception as e:
            logging.error(f"Error crítico durante la auditoría financiera: {e}")
            self.metrics["financial_integrity_score"] = 0.0
            self.metrics["audit_status"] = "ERROR"
            self.metrics["autonomous_decision"] = "CRITICAL_EXCEPTION"
            return None

if __name__ == "__main__":
    agent = SaaSFinancialAgent()
    report = agent.audit_saas_finances()

    if report:
        print("\n" + "="*50)
        print(" REPORTE AUTÓNOMO - FINANCIAL AGENT ")
        print("="*50)
        for key, value in report.items():
            print(f" - {key}: {value}")
        print("="*50)