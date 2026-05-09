import datetime

class DataValidatorQA:
    def __init__(self):
        self.error_log = []
        self.valid_records = 0

    def run_qa_pipeline(self, dataset):
        print(f"[{datetime.datetime.now()}] Starting QA Validation Pipeline...")
        
        for record in dataset:
            if self._validate_record(record):
                self.valid_records += 1
                
        return self.generate_report()

    def _validate_record(self, record):
        # Kural 1: Boş veri (Null) veya Eksik Alan Kontrolü
        if not record.get("transaction_id") or not record.get("amount"):
            self.error_log.append(f"FAIL: Missing critical data -> {record}")
            return False
            
        # Kural 2: Mantıksal Hata Kontrolü (Negatif işlem yapılamaz)
        if record.get("amount") <= 0:
            self.error_log.append(f"FAIL: Negative/Zero amount -> ID: {record['transaction_id']}")
            return False
            
        # Kural 3: Veri Tipi (Type) Kontrolü (Boolean beklenen yere String gelmiş mi?)
        if not isinstance(record.get("is_active"), bool):
            self.error_log.append(f"FAIL: Invalid data type for 'is_active' -> ID: {record['transaction_id']}")
            return False
            
        return True

    def generate_report(self):
        return {
            "total_processed": self.valid_records + len(self.error_log),
            "passed_qa": self.valid_records,
            "failed_qa": len(self.error_log),
            "errors": self.error_log
        }

# Sistem için Test Verisi (Mock Data)
if __name__ == "__main__":
    mock_data = [
        {"transaction_id": "T1001", "amount": 1500.50, "is_active": True},
        {"transaction_id": "T1002", "amount": -50.00, "is_active": True}, # Hatalı: Negatif miktar
        {"transaction_id": "T1003", "amount": 300.00, "is_active": "Yes"}, # Hatalı: Boolean yerine String
        {"transaction_id": None, "amount": 500.00, "is_active": True}      # Hatalı: ID eksik
    ]

    qa_system = DataValidatorQA()
    report = qa_system.run_qa_pipeline(mock_data)
    
    print("\n--- QA AUTOMATION REPORT ---")
    for key, value in report.items():
        print(f"{key.upper()}: {value}")
