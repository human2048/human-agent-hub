import os
import re

class CodeQualityAgent:
    """
    Code Quality & Frontend Agent (code_quality_agent.py)
    Dominio: Interfaz de Usuario y Estándares de Código.
    Audita y valida archivos HTML/CSS garantizando estándares HTML5,
    adaptabilidad móvil (Mobile-First) y optimización en menu-viewer.html.
    """
    def __init__(self, frontend_dir="frontend"):
        self.frontend_dir = frontend_dir

    def audit_html_file(self, file_name: str = "menu-viewer.html") -> dict:
        """
        Inspecciona el archivo HTML del visor de menús y verifica
        el cumplimiento de estándares esenciales de la plataforma.
        """
        file_path = os.path.join(self.frontend_dir, file_name)
        
        # Si el archivo está en la raíz, intentar encontrarlo allí
        if not os.path.exists(file_path) and os.path.exists(file_name):
            file_path = file_name

        if not os.path.exists(file_path):
            return {
                "agent": "CodeQualityAgent",
                "status": "ERROR_FILE_NOT_FOUND",
                "file": file_name,
                "passed_checks": False
            }

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Chequeos de auditoría de código HTML5 y Responsive Design
        checks = {
            "has_doctype": bool(re.search(r"<!DOCTYPE\s+html>", content, re.IGNORECASE)),
            "has_html_tag": bool(re.search(r"<html[^>]*>", content, re.IGNORECASE)),
            "has_head_tag": bool(re.search(r"<head[^>]*>", content, re.IGNORECASE)),
            "has_body_tag": bool(re.search(r"<body[^>]*>", content, re.IGNORECASE)),
            "has_viewport_meta": "viewport" in content.lower(),
            "has_charset_utf8": "utf-8" in content.lower(),
            "has_whatsapp_button_hook": "whatsapp" in content.lower() or "pedir" in content.lower()
        }

        # Evaluación general
        failed_checks = [check for check, passed in checks.items() if not passed]
        is_compliant = len(failed_checks) == 0

        report = {
            "agent": "CodeQualityAgent",
            "status": "FRONTEND_AUDIT_PASSED" if is_compliant else "FRONTEND_AUDIT_WARNING",
            "file": file_name,
            "passed_checks": is_compliant,
            "audit_details": checks,
            "missing_elements": failed_checks
        }

        status_icon = "🎨 [CodeQualityAgent] ✅" if is_compliant else "🎨 [CodeQualityAgent] ⚠️"
        print(f"{status_icon} Auditoría en '{file_name}': {'APROBADA' if is_compliant else 'REVISIÓN REQUERIDA'}")
        if failed_checks:
            print(f"   ⚠️ Elementos faltantes: {', '.join(failed_checks)}")

        return report

if __name__ == "__main__":
    # Test aislado con creación de un menu-viewer.html de prueba optimizado
    agent = CodeQualityAgent(".")
    
    # Crear un archivo HTML base para la prueba
    sample_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menú Digital Mobile-First</title>
</head>
<body>
    <div id="menu-container">
        <h1>Mi Comercio Local</h1>
        <button id="btn-whatsapp">Pedir por WhatsApp</button>
    </div>
</body>
</html>"""
    
    with open("menu-viewer.html", "w", encoding="utf-8") as f:
        f.write(sample_html)

    # Auditar el archivo creado
    agent.audit_html_file("menu-viewer.html")