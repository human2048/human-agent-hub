import os
import sys
from typing import List, Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class CleanerAgent:
    """
    Agente Limpiador (backend/cleaner_agent.py)
    Dominio: Saneamiento, normalización y formato de datos de catálogos y menús CSV.
    """
    def __init__(self):
        pass

    def clean_catalog_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia y normaliza la lista de productos del catálogo de menú."""
        cleaned = []
        for item in raw_data:
            name = str(item.get("item", "")).strip().title()
            price_raw = str(item.get("price", "0")).replace(".", "").replace("$", "").strip()
            
            try:
                price = float(price_raw)
            except ValueError:
                price = 0.0

            cleaned.append({
                "item": name,
                "price": price,
                "formatted_price": f"${price:,.2f}"
            })
            
        print(f"🧹 [CleanerAgent] Saneados {len(cleaned)} elementos del catálogo.")
        return cleaned

    def process_catalog(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Alias para mantener compatibilidad."""
        return self.clean_catalog_data(raw_data)

if __name__ == "__main__":
    cleaner = CleanerAgent()
    sample = [{"item": " hamburguesa ", "price": "15.000"}]
    print(cleaner.clean_catalog_data(sample))