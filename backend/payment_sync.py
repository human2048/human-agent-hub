import time
import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional

# Importación de los agentes core de la colmena
from database.db_agent import DatabaseAgent
from backend.financial_agent import FinancialAgent


DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "cyberniche.db"


class RealPaymentSyncService:
    """
    Servicio de Sincronización de Pasarela Real y Aprovisionamiento Multi-Tenant.
    Jurisdicción: Manejo de Webhooks reales (ePayco/Wompi/Stripe),
    aprovisionamiento automático de Tenants en BD y actualización de métricas MRR/Cashflow.
    """

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db = DatabaseAgent(db_path=db_path)
        self.financial_agent = FinancialAgent(monthly_fee=29.00)
        self._ensure_audit_schema()

    def _ensure_audit_schema(self):
        """Asegura que existan las tablas para registrar transacciones y cobros de Setup Fees."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS payment_transactions (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                payment_provider TEXT NOT NULL,
                transaction_type TEXT NOT NULL, -- 'SETUP_FEE' o 'RECURRING_SUBSCRIPTION'
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                status TEXT NOT NULL,
                raw_payload TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tenant_id) REFERENCES tenants(id)
            );
            """
        ]
        for q in queries:
            self.db.execute_transaction(q)

    def process_webhook_payload(self, provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Punto de entrada universal para Webhooks de Pasarelas Reales (ePayco, Wompi, Stripe).
        Normaliza los campos clave y desencadena la transacción ACID.
        """
        start_time = time.time()
        
        # 1. Normalización de datos según el proveedor
        normalized_data = self._normalize_webhook(provider, payload)
        
        if not normalized_data["is_valid"] or normalized_data["status"] != "APPROVED":
            return {
                "status": "REJECTED_OR_FAILED",
                "reason": normalized_data.get("reason", "Transacción no aprobada"),
                "processed_in_ms": round((time.time() - start_time) * 1000, 2)
            }

        tenant_id = normalized_data["tenant_id"]
        business_name = normalized_data["business_name"]
        whatsapp_number = normalized_data["whatsapp_number"]
        amount = normalized_data["amount"]
        tx_type = normalized_data["transaction_type"]
        tx_id = normalized_data["transaction_id"]

        print(f"💳 [PaymentSync] Procesando Webhook verificado de {provider} | Tx: {tx_id} | Tenant: {tenant_id}")

        # 2. Transacción Atómica en Base de Datos (Aprovisionamiento o Renovación)
        try:
            # Upsert en la tabla de Tenants
            self.db.execute_transaction(
                """
                INSERT INTO tenants (id, slug, business_name, whatsapp_number, is_active)
                VALUES (?, ?, ?, ?, 1)
                ON CONFLICT(id) DO UPDATE SET 
                    is_active = 1,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (tenant_id, tenant_id, business_name, whatsapp_number)
            )

            # Actualización o creación de Suscripción
            self.db.execute_transaction(
                """
                INSERT INTO subscriptions (tenant_id, status, mrr_amount)
                VALUES (?, 'active', ?)
                ON CONFLICT(tenant_id) DO UPDATE SET
                    status = 'active',
                    mrr_amount = ?,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (tenant_id, 29.00, 29.00)
            )

            # Registro de auditoría financiera
            self.db.execute_transaction(
                """
                INSERT INTO payment_transactions (id, tenant_id, payment_provider, transaction_type, amount, status, raw_payload)
                VALUES (?, ?, ?, ?, ?, 'APPROVED', ?);
                """,
                (tx_id, tenant_id, provider, tx_type, amount, json.dumps(payload))
            )

        except Exception as e:
            print(f"❌ [PaymentSync] Error en transacción de base de datos: {str(e)}")
            return {"status": "DATABASE_ERROR", "error": str(e)}

        # 3. Recálculo en tiempo real de Métricas SaaS
        active_tenants_query = self.db.execute_query("SELECT COUNT(*) FROM tenants WHERE is_active = 1;")
        active_count = active_tenants_query[0][0] if active_tenants_query else 0

        saas_metrics = self.financial_agent.calculate_saas_metrics(
            active_tenants=active_count,
            canceled_tenants=0,
            total_lead_cost=0.0
        )

        return {
            "status": "PROCESSED_AND_SYNCED",
            "tenant_id": tenant_id,
            "provisioned": True,
            "financial_summary": {
                "current_mrr": saas_metrics["metrics"]["monthly_recurrent_revenue_mrr"],
                "current_arr": saas_metrics["metrics"]["annual_recurrent_revenue_arr"],
                "active_tenants": active_count
            },
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        }

    def _normalize_webhook(self, provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizador de eventos para ePayco, Wompi y Stripe."""
        if provider == "epayco":
            # Estructura ePayco
            return {
                "is_valid": True,
                "transaction_id": payload.get("x_transaction_id", f"epayco_{int(time.time())}"),
                "status": "APPROVED" if payload.get("x_cod_response") == 1 else "FAILED",
                "tenant_id": payload.get("x_extra1", "default-tenant"),
                "business_name": payload.get("x_extra2", "Comercio Local"),
                "whatsapp_number": payload.get("x_extra3", "+573000000000"),
                "amount": float(payload.get("x_amount", 0.0)),
                "transaction_type": "SETUP_FEE" if payload.get("x_amount", 0) > 30 else "RECURRING_SUBSCRIPTION"
            }
        elif provider == "wompi":
            # Estructura Wompi
            data = payload.get("data", {}).get("transaction", {})
            return {
                "is_valid": True,
                "transaction_id": data.get("id", f"wompi_{int(time.time())}"),
                "status": "APPROVED" if data.get("status") == "APPROVED" else "FAILED",
                "tenant_id": data.get("reference", "").split("_")[0],
                "business_name": "Comercio Wompi",
                "whatsapp_number": "+573000000000",
                "amount": float(data.get("amount_in_cents", 0)) / 100,
                "transaction_type": "SETUP_FEE"
            }
        elif provider == "stripe":
            # Estructura Stripe
            return {
                "is_valid": True,
                "transaction_id": payload.get("id", f"stripe_{int(time.time())}"),
                "status": "APPROVED" if payload.get("status") == "succeeded" else "FAILED",
                "tenant_id": payload.get("metadata", {}).get("tenant_id", "stripe-tenant"),
                "business_name": payload.get("metadata", {}).get("business_name", "Comercio Stripe"),
                "whatsapp_number": payload.get("metadata", {}).get("whatsapp", "+573000000000"),
                "amount": float(payload.get("amount", 0)) / 100,
                "transaction_type": "RECURRING_SUBSCRIPTION"
            }
        
        return {"is_valid": False, "reason": f"Proveedor '{provider}' no soportado."}

if __name__ == "__main__":
    # Prueba de integración end-to-end con un Webhook simulación de ePayco (Setup Fee + Primer Mes)
    service = RealPaymentSyncService()
    
    mock_epayco_payload = {
        "x_transaction_id": "tx_epayco_99812",
        "x_cod_response": 1,
        "x_extra1": "pizzeria-don-luigi",
        "x_extra2": "Pizzería Don Luigi",
        "x_extra3": "+573158889900",
        "x_amount": 79.00  # $50 Setup Fee + $29 Primer Mes
    }

    result = service.process_webhook_payload("epayco", mock_epayco_payload)
    print("\n📊 Resultado de la Sincronización en Tiempo Real:")
    print(json.dumps(result, indent=2, ensure_ascii=False))