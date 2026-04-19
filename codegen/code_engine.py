import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK_PATH = os.path.join(BASE_DIR, "day-10-task-system", "tasks", "versions", "tasks_20260413_140855.json")


def load_tasks(path):
   with open(path, "r", encoding="utf-8") as f:
       return json.load(f)

def save_code_objects(code_objects):
   os.makedirs(os.path.join(BASE_DIR, "codegen", "versions"), exist_ok=True)

   ts = datetime.now().strftime("%Y%m%d_%H%M%S")
   path = os.path.join(BASE_DIR, "codegen", "versions", f"code_{ts}.json")

   with open(path, "w", encoding="utf-8") as f:
       json.dump(code_objects, f, indent=2)

   return path

from code_generator import generate_code_objects
from code_reviewer import review_code
from code_improver import improve_code_object


def build_code_pipeline():
   tasks = load_tasks(TASK_PATH)

   code_objects = generate_code_objects(tasks)

   for i, code_obj in enumerate(code_objects):
       first_review = review_code(code_obj)
       code_obj["review"] = first_review

       if not first_review["valid"]:
           improved = improve_code_object(code_obj)
           second_review = review_code(improved)
           improved["review"] = second_review
           code_objects[i] = improved

   path = save_code_objects(code_objects)
   print("Saved code objects to:", path)

   return code_objects

if __name__ == "__main__":
   code_objects = build_code_pipeline()

   print("\n--- CODE OBJECTS ---")
   for obj in code_objects[:5]:
       print({
           "feature": obj["feature"],
           "task": obj["task"],
           "task_type": obj["task_type"],
           "review": obj["review"]
       })
