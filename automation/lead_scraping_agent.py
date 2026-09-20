import os
import sys
from typing import List, Dict, Any

# Asegurar importación del directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class LeadScrapingAgent:
    """
    Agente de Adquisición B2B (automation/lead_scraping_agent.py)
    Dominio: Prospección y recolección de leads de comercios locales.
    """
    def __init__(self):
        pass

    def scrape_leads(self, category: str = "Restaurantes") -> List[Dict[str, Any]]:
        """Scrapea y filtra prospectos locales según la categoría especificada."""
        mock_leads = [
            {
                "business_name": "Restaurante El Gourmet",
                "phone": "+573015550199",
                "category": category,
                "status": "VALID"
            },
            {
                "business_name": "Café Central",
                "phone": "+573025550288",
                "category": category,
                "status": "VALID"
            }
        ]
        
        scraped = len(mock_leads)
        valid = len([l for l in mock_leads if l["status"] == "VALID"])
        duplicates = scraped - valid

        print(f"🎯 [LeadScrapingAgent] Scrapeados: {scraped} | Leads Válidos: {valid} | Descartados/Duplicados: {duplicates}")
        return mock_leads

    def run_scraping_pipeline(self, category: str = "Restaurantes") -> List[Dict[str, Any]]:
        """Alias para mantener compatibilidad."""
        return self.scrape_leads(category)

if __name__ == "__main__":
    agent = LeadScrapingAgent()
    print(agent.scrape_leads("Restaurantes"))