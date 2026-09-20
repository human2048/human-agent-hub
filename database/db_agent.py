import sqlite3
import os

class DatabaseAgent:
    """
    Agente de Base de Datos (database/db_agent.py)
    Gestiona la persistencia SQLite multi-tenant.
    """
    def __init__(self, db_path: str = "cyberniche.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa las tablas base si no existen."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de clientes/tenants
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def init_db(self):
        """Alias público de inicialización para el orquestador."""
        self._init_db()

if __name__ == "__main__":
    db = DatabaseAgent()
    print("✅ Base de datos inicializada correctamente.")