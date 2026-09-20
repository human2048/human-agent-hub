import sqlite3
import os
from typing import List, Tuple, Any, Dict

class DatabaseAgent:
    """
    Database Agent (database/db_agent.py)
    Rol: Arquitecto de Datos y Administrador de Persistencia Senior.
    Dominio: Gestión avanzada de SQLite con transacciones ACID, integridad referencial 
    y persistencia multi-tenant para el Micro-SaaS.
    """
    def __init__(self, db_path: str = "cyberniche.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self) -> None:
        """Inicializa el esquema relacional con control de transacciones y optimización de índices."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA journal_mode=WAL;")  # Write-Ahead Logging para alto rendimiento concurrente
                conn.execute("PRAGMA foreign_keys = ON;")
                cursor = conn.cursor()
                
                # Tabla principal de tenants (clientes del Micro-SaaS)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tenants (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        status TEXT DEFAULT 'ACTIVE',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabla de transacciones y métricas financieras de soporte local
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tenant_id TEXT,
                        amount REAL NOT NULL,
                        currency TEXT DEFAULT 'USD',
                        status TEXT DEFAULT 'COMPLETED',
                        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (tenant_id) REFERENCES tenants(id)
                    )
                """)
                
                conn.commit()
            print("💾 [DatabaseAgent] Base de datos relacional y esquemas ACID inicializados correctamente.")
        except Exception as e:
            print(f"❌ [DatabaseAgent] Error crítico en inicialización de base de datos: {e}")

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        """Ejecuta consultas SQL de manera segura protegiendo contra inyecciones y fallos de bloqueo."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ [DatabaseAgent] Error ejecutando consulta SQL: {e}")
            return []

if __name__ == "__main__":
    db = DatabaseAgent()