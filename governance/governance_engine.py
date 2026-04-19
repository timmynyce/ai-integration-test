import json
import os
from datetime import datetime

from validation import validate_integration_input
from guardrails import apply_output_guardrails
from logger import write_log


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INTEGRATION_PATH = os.path.join(
   BASE_DIR,
   "integrations",
   "versions",
   "integrations_20260418_143718.json"
)

def load_integration_results(path: str):
   with open(path, "r", encoding="utf-8") as f:
       return json.load(f)
def save_governed_results(results):
   output_dir = os.path.join(BASE_DIR, "governance")
   os.makedirs(output_dir, exist_ok=True)

   ts = datetime.now().strftime("%Y%m%d_%H%M%S")
   path = os.path.join(output_dir, f"governed_results_{ts}.json")

   with open(path, "w", encoding="utf-8") as f:
       json.dump(results, f, indent=2)

   return path

def govern_records(records):
   governed = []
   log_dir = os.path.join(BASE_DIR, "governance", "logs")

   for record in records:
       input_check = validate_integration_input(record)
       output_check = apply_output_guardrails(record)

       allowed_to_proceed = input_check["valid"] and output_check["valid"]

       governed_record = {
           "task": record.get("task", ""),
           "integration_target": record.get("integration_target", ""),
           "input_valid": input_check["valid"],
           "input_issues": input_check["issues"],
           "output_valid": output_check["valid"],
           "output_issues": output_check["issues"],
           "allowed_to_proceed": allowed_to_proceed,
           "log_status": "logged",
           "timestamp": datetime.now().isoformat()
       }

       write_log(log_dir, governed_record)
       governed.append(governed_record)

   return governed

def run_governance_pipeline():
   records = load_integration_results(INTEGRATION_PATH)

   governed_results = govern_records(records)

   allowed_count = sum(1 for r in governed_results if r["allowed_to_proceed"])
   blocked_count = len(governed_results) - allowed_count

   print(f"Allowed records: {allowed_count}")
   print(f"Blocked records: {blocked_count}")

   path = save_governed_results(governed_results)
   print("Saved governed results to:", path)

   return governed_results

if __name__ == "__main__":
   governed_results = run_governance_pipeline()

   print("\n--- SAMPLE GOVERNED RESULTS ---")
   for result in governed_results[:3]:
       print(result)
