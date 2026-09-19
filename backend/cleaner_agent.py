import os
import time
import psutil
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (DataCleanerAgent-Autonomous): %(message)s"
)

class DataCleanerAgent:
    def __init__(self, input_path: str, output_path: str = "data/cleaned_output.csv"):
        self.input_path = input_path
        self.output_path = output_path
        self.metrics = {
            "rows_processed": 0,
            "errors_found": 0,
            "integrity_rate": 0.0,
            "throughput_rows_per_sec": 0.0,
            "ram_usage_mb": 0.0,
            "errors_recovered": 0,
            "autonomous_decision": "PENDING"
        }

    def evaluate_and_decide(self):
        """
        Toma de decisión autónoma basada en el porcentaje de integridad detectado.
        """
        rate = self.metrics["integrity_rate"]
        if rate == 100.0:
            decision = "OPTIMAL_FLOW: Datos limpios, proceder a almacenamiento directo."
        elif rate >= 50.0:
            decision = "WARNING_FLOW: Aplicar limpieza estándar y registrar anomalías."
        else:
            decision = "CRITICAL_QUARANTINE: Integridad baja. Derivar archivo a cuarentena para revisión técnica."
        
        self.metrics["autonomous_decision"] = decision
        logging.info(f"Decisión Autónoma Ejecutada -> {decision}")

    def process_data(self, chunk_size: int = 10000):
        process = psutil.Process(os.getpid())
        start_time = time.time()
        
        if not os.path.exists(self.input_path):
            logging.error(f"El archivo de entrada '{self.input_path}' no existe.")
            self.metrics["autonomous_decision"] = "ABORT_FILE_NOT_FOUND"
            return None

        total_rows = 0
        valid_rows = 0
        error_count = 0
        cleaned_chunks = []

        try:
            logging.info(f"Iniciando auditoría autónoma desde: {self.input_path}")
            
            for chunk in pd.read_csv(self.input_path, chunksize=chunk_size, low_memory=False):
                total_rows += len(chunk)
                try:
                    initial_chunk_len = len(chunk)
                    chunk_cleaned = chunk.dropna()
                    dropped_rows = initial_chunk_len - len(chunk_cleaned)
                    
                    error_count += dropped_rows
                    valid_rows += len(chunk_cleaned)
                    cleaned_chunks.append(chunk_cleaned)
                except Exception as inner_e:
                    self.metrics["errors_recovered"] += 1
                    logging.warning(f"Excepción recuperada: {inner_e}")
                    continue

            if cleaned_chunks:
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                final_df = pd.concat(cleaned_chunks, ignore_index=True)
                final_df.to_csv(self.output_path, index=False)

            end_time = time.time()
            duration = end_time - start_time
            
            if duration > 0:
                self.metrics["throughput_rows_per_sec"] = round(total_rows / duration, 2)
            
            self.metrics["rows_processed"] = total_rows
            self.metrics["errors_found"] = error_count
            
            if total_rows > 0:
                self.metrics["integrity_rate"] = round((valid_rows / total_rows) * 100, 2)
            else:
                self.metrics["integrity_rate"] = 0.0

            self.metrics["ram_usage_mb"] = round(process.memory_info().rss / (1024 * 1024), 2)

            # Ejecutar el motor de decisión autónoma post-auditoría
            self.evaluate_and_decide()

            return self.metrics

        except Exception as e:
            logging.error(f"Error crítico: {e}")
            self.metrics["autonomous_decision"] = "CRITICAL_ERROR"
            return None

if __name__ == "__main__":
    agent = DataCleanerAgent(input_path="data/sample.csv")
    results = agent.process_data()
    if results:
        print("\n" + "="*50)
        print(" REPORTE AUTÓNOMO - DATA CLEANER AGENT ")
        print("="*50)
        for key, value in results.items():
            print(f" - {key}: {value}")
        print("="*50)