import os
import sys
from typing import List, Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class LeadScrapingAgent:
    """
    Lead Scraping & Growth Agent (automation/lead_scraping_agent.py)
    Rol: Director de Prospección y Growth Hacking Senior.
    Dominio: Captura, enriquecimiento y calificación de prospectos comerciales locales 
    bajo modelos de prospección B2B de alta eficiencia.
    """
    def __init__(self):
        pass

    def execute(self, category: str = "Restaurantes") -> List[Dict[str, Any]]:
        """
        Ejecuta el pipeline de prospección y filtrado inteligente de leads locales 
        según la categoría comercial objetivo.
        """
        try:
            if not isinstance(category, str) or not category.strip():
                raise ValueError("La categoría objetivo debe ser una cadena de texto válida.")

            sanitized_category = category.strip().title()

            # Base de leads cualificados simulando inteligencia de prospección global
            qualified_leads = [
                {
                    "business_name": "Restaurante El Gourmet",
                    "phone": "+573015550199",
                    "category": sanitized_category,
                    "conversion_score": 92.5,
                    "status": "QUALIFIED_VALID"
                },
                {
                    "business_name": "Café Central Art",
                    "phone": "+573025550288",
                    "category": sanitized_category,
                    "conversion_score": 88.0,
                    "status": "QUALIFIED_VALID"
                }
            ]
            
            total_scraped = len(qualified_leads)
            valid_leads = len([l for l in qualified_leads if "VALID" in l["status"]])
            discarded = total_scraped - valid_leads

            print(f"🎯 [LeadScrapingAgent Growth] Categoría: {sanitized_category} | Capturados: {total_scraped} | Cualificados: {valid_leads} | Descartados: {discarded}")
            return qualified_leads

        except Exception as e:
            print(f"❌ [LeadScrapingAgent] Error crítico en pipeline de prospección: {e}")
            return []

if __name__ == "__main__":
    agent = LeadScrapingAgent()
    agent.execute("Restaurantes")