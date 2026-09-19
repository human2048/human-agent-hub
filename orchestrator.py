import os
import time
import logging

from backend.cleaner_agent import DataCleanerAgent
from automation.monitoring_agent import MonitoringAgent
from automation.lead_scraping_agent import LeadScrapingAgent
from frontend.code_quality_agent import CodeQualityAgent
from database.db_agent import DatabaseAgent
from automation.integration_agent import IntegrationAgent
from backend.financial_agent import SaaSFinancialAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (CyberNicheOrchestrator-Autonomous): %(message)s"
)

class CyberNicheOrchestrator:
    def __init__(self):
        logging.info("Inicializando Núcleo de Orquestación Autónoma de CyberNiche Lab...")

    def run_master_cycle(self):
        start_time = time.time()
        master_report = {}

        print("\n" + "="*70)
        print(" INICIANDO CICLO OPERATIVO AUTÓNOMO MAESTRO - CYBERNICHE-LAB ")
        print("="*70)

        # 1. Database Agent
        logging.info("[1/7] Despachando Database & SQL Agent...")
        db_agent = DatabaseAgent()
        master_report["database"] = db_agent.initialize_and_audit()

        # 2. Monitoring Agent
        logging.info("[2/7] Despachando Monitoring & SRE Agent...")
        monitoring_agent = MonitoringAgent()
        master_report["monitoring"] = monitoring_agent.check_health()

        # 3. Data Cleaner Agent
        logging.info("[3/7] Despachando Data Cleaner Agent...")
        cleaner_agent = DataCleanerAgent(input_path="data/sample.csv")
        master_report["cleaner"] = cleaner_agent.process_data()

        # 4. Inbound Growth Agent
        logging.info("[4/7] Despachando Inbound Growth Agent...")
        growth_agent = LeadScrapingAgent(target_urls=["https://httpbin.org/html", "https://example.com"])
        _, master_report["growth"] = growth_agent.execute_scraping()

        # 5. Code Quality Agent
        logging.info("[5/7] Despachando Code Quality Agent...")
        frontend_agent = CodeQualityAgent(target_file="menu-viewer.html")
        master_report["frontend"] = frontend_agent.audit_frontend_code()

        # 6. Integration Agent
        logging.info("[6/7] Despachando Integration & Workflow Agent...")
        integration_agent = IntegrationAgent()
        sample_event = {"event_type": "MASTER_AUTONOMOUS_SYNC", "timestamp": time.time()}
        master_report["integration"] = integration_agent.trigger_workflow_event(sample_event)

        # 7. SaaS Financial Agent
        logging.info("[7/7] Despachando SaaS Financial Agent...")
        financial_agent = SaaSFinancialAgent()
        master_report["financial"] = financial_agent.audit_saas_finances()

        total_duration = round(time.time() - start_time, 2)

        # --- DASHBOARD EJECUTIVO AUTÓNOMO ---
        print("\n" + "="*70)
        print(f" DASHBOARD EJECUTIVO AUTÓNOMO UNIFICADO (Duración Ciclo: {total_duration}s) ")
        print("="*70)
        
        for module_name, metrics in master_report.items():
            print(f"\n -> MÓDULO: {module_name.upper()}")
            if metrics:
                for k, v in metrics.items():
                    print(f"    - {k}: {v}")
            else:
                print("    - Estado: SIN DATOS / ERROR CRÍTICO")
                
        print("\n" + "="*70)
        logging.info("Ciclo operativo autónomo maestro finalizado con éxito.")

if __name__ == "__main__":
    orchestrator = CyberNicheOrchestrator()
    orchestrator.run_master_cycle()