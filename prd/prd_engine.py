import os
import json
from datetime import datetime

from prd_generator import convert_prd_to_json
from prd_validator import validate_structured_prd
from prd_improver import improve_structured_prd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRD_PATH = os.path.join(BASE_DIR, "day-7-file-workflows", "sample_prd_complex.txt")

def read_text_file(path):
   with open(path, "r", encoding="utf-8") as f:
       return f.read()

def save_prd_version(prd):
   os.makedirs("prd/versions", exist_ok=True)

   ts = datetime.now().strftime("%Y%m%d_%H%M%S")
   path = f"prd/versions/prd_{ts}.json"

   with open(path, "w") as f:
       json.dump(prd, f, indent=2)

   return path

def build_structured_prd():
   prd_text = read_text_file(PRD_PATH)

   prd = convert_prd_to_json(prd_text)

   for i in range(3):
       validation = validate_structured_prd(prd)

       print(f"Iteration {i+1}:", validation)

       if validation["valid"]:
           break

       prd = improve_structured_prd(prd, validation["errors"])

   path = save_prd_version(prd)

   print("Saved to:", path)

   return prd

def cto_score(prd):
   score = 0

   if len(prd["features"]) >= 3:
       score += 2
   if len(prd["success_metrics"]) >= 2:
       score += 2
   if len(prd["edge_cases"]) >= 2:
       score += 2

   return score

def build_structured_prd_with_cto_gate():
   prd = build_structured_prd()

   score = cto_score(prd)
   print("CTO Score:", score)

   return prd

def prd_to_tasks(prd):
   tasks = []

   for f in prd["features"]:
       for r in f["requirements"]:
           tasks.append({
               "feature": f["name"],
               "task": r
           })

   return tasks

if __name__ == "__main__":
   final_prd = build_structured_prd_with_cto_gate()

   tasks = prd_to_tasks(final_prd)

   print("\nGenerated Tasks:")
   for task in tasks:
       print(task)
