import os
import sqlite3
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (DatabaseAgent-Autonomous): %(message)s"
)

class DatabaseAgent:
    def __init__(self, db_path: str = "database/cyberniche.db"):
        self.db_path = db_path
        self.metrics = {
            "queries_executed": 0,
            "transaction_success_rate": 0.0,
            "query_latency_ms": 0.0,
            "integrity_errors": 0,
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        """
        Toma de decisión autónoma basada en la tasa de éxito transaccional y errores de integridad.
        """
        success_rate = self.metrics["transaction_success_rate"]
        integrity_errs = self.metrics["integrity_errors"]

        if success_rate == 100.0 and integrity_errs == 0:
            decision = "DB_OPTIMAL: Operaciones transaccionales estables y esquema íntegro."
        elif success_rate >= 50.0:
            decision = "WARNING_DB_CONSTRAINTS: Se detectaron restricciones o duplicados controlados. Monitorear inserciones."
        else:
            decision = "CRITICAL_DB_FAILURE: Fallos transaccionales severos. Ejecutar rollback y aislamiento de datos."

        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma de Database Ejecutada -> {decision}")

    def initialize_and_audit(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        start_time = time.time()
        success_count = 0
        queries_count = 0

        try:
            logging.info(f"Conectando a la base de datos transaccional en: {self.db_path}")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            queries_count += 1
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    membership_status TEXT DEFAULT 'Inactive',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            success_count += 1

            queries_count += 1
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (email, membership_status) 
                    VALUES ('test_user@cyberniche.lab', 'Active')
                ''')
                conn.commit()
                success_count += 1
            except Exception as inner_e:
                self.metrics["integrity_errors"] += 1
                logging.warning(f"Restricción de integridad aplicada: {inner_e}")

            conn.close()
            end_time = time.time()

            self.metrics["queries_executed"] = queries_count
            self.metrics["query_latency_ms"] = round((end_time - start_time) * 1000, 2)
            
            if queries_count > 0:
                self.metrics["transaction_success_rate"] = round((success_count / queries_count) * 100, 2)

            # Ejecutar evaluación y decisión autónoma
            self.evaluate_and_decide()

            logging.info("Auditoría de base de datos transaccional autónoma completada.")
            return self.metrics

        except Exception as e:
            logging.error(f"Error crítico operando la base de datos: {e}")
            self.metrics["integrity_errors"] += 1
            self.metrics["autonomous_decision"] = "CRITICAL_DB_EXCEPTION"
            return None

if __name__ == "__main__":
    agent = DatabaseAgent()
    report = agent.initialize_and_audit()

    if report:
        print("\n" + "="*50)
        print(" REPORTE AUTÓNOMO - DATABASE AGENT ")
        print("="*50)
        for key, value in report.items():
            print(f" - {key}: {value}")
        print("="*50)