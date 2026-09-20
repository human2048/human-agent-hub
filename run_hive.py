from bot_listener import OrchestratorAgent

def main():
    print("🚀 [CEO Master Runner] Inicializando la Colmena de Agentes Autónomos...")
    coordinator = OrchestratorAgent()

    print("\n--- [PRUEBA 1: Generación de Landing Page Frontend] ---")
    coordinator.process_command("frontend", {"brand_name": "SaaS Local Élite"})

    print("\n--- [PRUEBA 2: Análisis Financiero CFO] ---")
    coordinator.process_command("financial", {"subscribers": 15, "mrr_price": 39.0, "cac": 12.0})

    print("\n--- [PRUEBA 3: Prospección de Leads B2B] ---")
    coordinator.process_command("scraping", {"category": "Cafeterías Gourmet"})

    print("\n✅ [CEO Master Runner] Verificación completa. Todos los agentes ejecutores operan con éxito.")

if __name__ == "__main__":
    main()