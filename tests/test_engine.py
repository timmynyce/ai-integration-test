import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_PATH = os.path.join(BASE_DIR, "codegen", "versions", "code_20260413_151744.json")

def load_code_objects(path):
   with open(path, "r", encoding="utf-8") as f:
       return json.load(f)

def save_tests(tests):
   os.makedirs(os.path.join(BASE_DIR, "tests", "versions"), exist_ok=True)

   ts = datetime.now().strftime("%Y%m%d_%H%M%S")
   path = os.path.join(BASE_DIR, "tests", "versions", f"tests_{ts}.json")

   with open(path, "w", encoding="utf-8") as f:
       json.dump(tests, f, indent=2)

   return path

from test_generator import generate_test_cases
from test_validator import validate_tests


def build_test_pipeline():
   code_objects = load_code_objects(CODE_PATH)

   tests = generate_test_cases(code_objects)

   validation = validate_tests(tests)
   print("Validation:", validation)

   path = save_tests(tests)
   print("Saved tests to:", path)

   return tests

if __name__ == "__main__":
   tests = build_test_pipeline()

   print("\n--- TESTS ---")
   for t in tests[:5]:
       print(t)
