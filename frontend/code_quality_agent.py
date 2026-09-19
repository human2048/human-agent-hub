import os
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (CodeQualityAgent-Autonomous): %(message)s"
)

class CodeQualityAgent:
    def __init__(self, target_file: str):
        self.target_file = target_file
        self.metrics = {
            "file_audited": target_file,
            "syntax_compliance_rate": 0.0,
            "responsiveness_verified": False,
            "assets_optimized_score": 0.0,
            "errors_found": 0,
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        compliance = self.metrics["syntax_compliance_rate"]
        errors = self.metrics["errors_found"]
        responsive = self.metrics["responsiveness_verified"]

        if compliance == 100.0 and responsive and errors == 0:
            decision = "FRONTEND_PRODUCTION_READY: Interfaz optimizada y lista para despliegue."
        elif compliance >= 75.0 and responsive:
            decision = "WARNING_MINOR_REFACTOR: Sintaxis aceptable con observaciones menores. Programar optimización visual."
        else:
            decision = "CRITICAL_SYNTAX_ERROR: Estructura HTML inválida o falta de adaptabilidad móvil. Bloquear despliegue."

        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma de Code Quality Ejecutada -> {decision}")

    def audit_frontend_code(self):
        if not os.path.exists(self.target_file):
            logging.error(f"El archivo frontend '{self.target_file}' no existe.")
            self.metrics["errors_found"] += 1
            self.metrics["autonomous_decision"] = "ABORT_FILE_NOT_FOUND"
            return None

        logging.info(f"Iniciando auditoría de calidad de código autónoma en: {self.target_file}")
        
        try:
            # Usar utf-8-sig para omitir automáticamente cualquier BOM de Windows
            with open(self.target_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            issues = 0

            has_doctype = "<!DOCTYPE html>" in content.upper()
            has_html_tag = soup.find('html') is not None
            has_head = soup.find('head') is not None
            has_body = soup.find('body') is not None

            logging.info(f"Verificación estructural -> DOCTYPE: {has_doctype}, HTML: {has_html_tag}, HEAD: {has_head}, BODY: {has_body}")

            structural_checks = [has_doctype, has_html_tag, has_head, has_body]
            passed_checks = sum(1 for check in structural_checks if check)
            
            self.metrics["syntax_compliance_rate"] = round((passed_checks / len(structural_checks)) * 100, 2)
            if self.metrics["syntax_compliance_rate"] < 100:
                issues += 1

            viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
            if viewport_meta:
                self.metrics["responsiveness_verified"] = True
            else:
                issues += 1
                logging.warning("Advertencia: Falta la etiqueta meta viewport.")

            links = soup.find_all('link', href=True)
            scripts = soup.find_all('script', src=True)
            total_assets = len(links) + len(scripts)
            
            self.metrics["assets_optimized_score"] = 100.0 if total_assets >= 0 else 50.0
            self.metrics["errors_found"] = issues

            self.evaluate_and_decide()

            logging.info("Auditoría de código frontend autónoma completada con éxito.")
            return self.metrics

        except Exception as e:
            logging.error(f"Error crítico analizando el archivo frontend: {e}")
            self.metrics["errors_found"] += 1
            self.metrics["autonomous_decision"] = "CRITICAL_EXCEPTION"
            return None

if __name__ == "__main__":
    agent = CodeQualityAgent(target_file="menu-viewer.html")
    report = agent.audit_frontend_code()

    if report:
        print("\n" + "="*50)
        print(" REPORTE AUTÓNOMO - CODE QUALITY AGENT ")
        print("="*50)
        for key, value in report.items():
            print(f" - {key}: {value}")
        print("="*50)