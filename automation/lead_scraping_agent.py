import os
import time
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (LeadScrapingAgent-Autonomous): %(message)s"
)

class LeadScrapingAgent:
    def __init__(self, target_urls: list):
        self.target_urls = target_urls
        self.metrics = {
            "urls_targeted": len(target_urls),
            "successful_extractions": 0,
            "extraction_success_rate": 0.0,
            "leads_collected": 0,
            "duplicates_filtered": 0,
            "data_completeness_rate": 0.0,
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        """
        Toma de decisión autónoma basada en la tasa de éxito de extracción y completitud de datos.
        """
        success_rate = self.metrics["extraction_success_rate"]
        completeness = self.metrics["data_completeness_rate"]

        if success_rate == 100.0 and completeness >= 75.0:
            decision = "GROWTH_OPTIMAL: Campaña efectiva. Continuar inyección de leads a base de datos."
        elif success_rate >= 50.0:
            decision = "WARNING_PARTIAL_DATA: Extracción parcial completada. Ajustar selectores de parsing web."
        else:
            decision = "CRITICAL_SCRAPING_BLOCK: Alta tasa de fallo o bloqueo de red detectada. Rotar proxies o reintentar."

        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma de Growth Ejecutada -> {decision}")

    def execute_scraping(self):
        collected_leads = []
        seen_identifiers = set()
        successful = 0

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberNicheLabAgent/1.0"
        }

        logging.info("Iniciando campaña de adquisición y scraping autónomo de leads...")

        for url in self.target_urls:
            try:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    successful += 1
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else "Sin Título"
                    
                    lead_item = {
                        "source_url": url,
                        "title": title.strip(),
                        "status": "Qualifying"
                    }

                    identifier = lead_item["title"]
                    if identifier in seen_identifiers:
                        self.metrics["duplicates_filtered"] += 1
                    else:
                        seen_identifiers.add(identifier)
                        collected_leads.append(lead_item)
                        
                    time.sleep(1)
                else:
                    logging.warning(f"Fallo de extracción en {url} - Código HTTP: {response.status_code}")
            except Exception as e:
                logging.error(f"Error conectando a la URL {url}: {e}")

        self.metrics["successful_extractions"] = successful
        self.metrics["leads_collected"] = len(collected_leads)

        if self.metrics["urls_targeted"] > 0:
            self.metrics["extraction_success_rate"] = round((successful / self.metrics["urls_targeted"]) * 100, 2)
        
        if collected_leads:
            complete_leads = sum(1 for lead in collected_leads if lead["title"] != "Sin Título")
            self.metrics["data_completeness_rate"] = round((complete_leads / len(collected_leads)) * 100, 2)

        # Ejecutar evaluación y decisión autónoma
        self.evaluate_and_decide()

        logging.info("Campaña de Growth autónoma finalizada.")
        return collected_leads, self.metrics

if __name__ == "__main__":
    sample_targets = [
        "https://httpbin.org/html",
        "https://example.com"
    ]

    agent = LeadScrapingAgent(target_urls=sample_targets)
    _, report = agent.execute_scraping()

    print("\n" + "="*50)
    print(" REPORTE AUTÓNOMO - GROWTH AGENT ")
    print("="*50)
    for key, value in report.items():
        print(f" - {key}: {value}")
    print("="*50)