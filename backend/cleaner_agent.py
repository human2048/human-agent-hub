import os
import sys
from typing import List, Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class CleanerAgent:
    """
    Cleaner Agent (backend/cleaner_agent.py)
    Rol: Ingeniero de Datos y Saneamiento Senior.
    Dominio: Pipeline automatizado de normalización, limpieza tipográfica, validación 
    de esquemas y saneamiento preventivo de catálogos y entradas de usuario.
    """
    def __init__(self):
        pass

    def execute(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta un pipeline de saneamiento determinista sobre catálogos o listados comerciales,
        garantizando tipado estricto y eliminación de caracteres anómalos.
        """
        cleaned_records = []
        try:
            if not isinstance(raw_data, list):
                raise TypeError("El flujo de entrada (raw_data) debe ser estrictamente una lista de diccionarios.")

            for index, item in enumerate(raw_data):
                if not isinstance(item, dict):
                    print(f"⚠️ [CleanerAgent] Advertencia: El elemento en el índice {index} no es un diccionario válido. Omitiendo.")
                    continue

                # Normalización de textos (Capitalización limpia, eliminación de espacios excesivos)
                raw_name = item.get("item", item.get("name", "Desconocido"))
                name = str(raw_name).strip().title()
                
                # Normalización financiera de precios (Remoción segura de símbolos y puntos de miles)
                price_raw = str(item.get("price", "0")).replace(".", "").replace("$", "").replace(",", "").strip()
                
                try:
                    price = float(price_raw)
                    if price < 0:
                        price = 0.0
                except ValueError:
                    price = 0.0

                cleaned_records.append({
                    "item": name,
                    "price": round(price, 2),
                    "formatted_price": f"${price:,.2f}",
                    "status": "SANITIZED"
                })
                
            print(f"🧹 [CleanerAgent] Pipeline completado. Saneados y normalizados {len(cleaned_records)} registros con éxito.")
            return cleaned_records

        except Exception as e:
            print(f"❌ [CleanerAgent] Error crítico en el pipeline de saneamiento: {e}")
            return []

if __name__ == "__main__":
    agent = CleanerAgent()
    sample_data = [
        {"item": "  hamburguesa artesanal  ", "price": "15.000"},
        {"item": "refresco personal", "price": "$4.500"}
    ]
    agent.execute(sample_data)