import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from typing import Any, List, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "cyberniche.db"
SANDBOX_ROOT = PROJECT_ROOT / "sandbox" / "sandbox_practica"


def validate_sandbox_path(path: str | Path) -> Path:
    """Return a canonical sandbox path or reject paths outside the sandbox."""
    sandbox_root = SANDBOX_ROOT.resolve()
    candidate = Path(path)
    resolved = candidate.resolve()
    if not resolved.is_relative_to(sandbox_root):
        raise PermissionError(
            f"Ruta fuera del sandbox bloqueada: {candidate}"
        )
    return resolved


class DatabaseAgent:
    """
    Database Agent (database/db_agent.py)
    Rol: Arquitecto de Datos y Administrador de Persistencia Senior.
    Dominio: Gestión avanzada de SQLite con transacciones ACID, integridad referencial 
    y persistencia multi-tenant para el Micro-SaaS.
    """
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        """Open a configured SQLite connection with WAL enabled."""
        connection = sqlite3.connect(self.db_path, timeout=30)
        connection.execute("PRAGMA journal_mode=WAL;")
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    def init_db(self) -> None:
        """Inicializa el esquema relacional con control de transacciones y optimización de índices."""
        try:
            with closing(self._connect()) as conn:
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
            with closing(self._connect()) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ [DatabaseAgent] Error ejecutando consulta SQL: {e}")
            return []

    def execute_transaction(
        self, query: str, params: Tuple[Any, ...] = ()
    ) -> None:
        """Execute a write query using the same WAL-enabled connection policy."""
        with closing(self._connect()) as conn:
            conn.execute(query, params)
            conn.commit()


def run_integrity_check() -> None:
    """Verify WAL persistence and sandbox containment using temporary artifacts."""
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=SANDBOX_ROOT) as temp_dir:
        temp_root = Path(temp_dir)
        database = DatabaseAgent(temp_root / "integrity_check.db")
        with closing(database._connect()) as connection:
            journal_mode = connection.execute(
                "PRAGMA journal_mode;"
            ).fetchone()[0]
        if str(journal_mode).lower() != "wal":
            raise AssertionError(f"WAL no habilitado: {journal_mode}")

        database.execute_transaction(
            "INSERT INTO tenants (id, name) VALUES (?, ?)",
            ("integrity-check", "Integrity Check"),
        )
        result = database.execute_query(
            "SELECT name FROM tenants WHERE id = ?", ("integrity-check",)
        )
        if result != [("Integrity Check",)]:
            raise AssertionError(f"Lectura SQLite inesperada: {result}")

        test_file = validate_sandbox_path(temp_root / "sandbox_test.txt")
        test_file.write_text("sandbox-ok", encoding="utf-8")
        if test_file.read_text(encoding="utf-8") != "sandbox-ok":
            raise AssertionError("No se pudo verificar el archivo del sandbox")

        try:
            validate_sandbox_path(SANDBOX_ROOT / ".." / "outside.txt")
        except PermissionError:
            pass
        else:
            raise AssertionError("Traversal fuera del sandbox no fue bloqueado")

    print("✅ Integridad verificada: SQLite WAL y sandbox operativos.")

if __name__ == "__main__":
    run_integrity_check()