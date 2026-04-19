import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STORY_PATH = os.path.join(BASE_DIR, "stories", "versions", "stories_20260413_105506.json")

def load_stories(path):
   with open(path, "r", encoding="utf-8") as f:
       return json.load(f)

def save_tasks(tasks):
   os.makedirs("tasks/versions", exist_ok=True)

   ts = datetime.now().strftime("%Y%m%d_%H%M%S")
   path = f"tasks/versions/tasks_{ts}.json"

   with open(path, "w", encoding="utf-8") as f:
       json.dump(tasks, f, indent=2)

   return path

from task_generator import generate_tasks
from task_validator import validate_tasks
from task_improver import improve_tasks


def build_tasks():
   stories = load_stories(STORY_PATH)

   tasks = generate_tasks(stories)

   validation = validate_tasks(tasks)
   print("Iteration 1:", validation)

   if not validation["valid"]:
       tasks = improve_tasks(tasks)
       validation = validate_tasks(tasks)
       print("Iteration 2:", validation)

   path = save_tasks(tasks)
   print("Saved tasks to:", path)

   return tasks

if __name__ == "__main__":
   tasks = build_tasks()

   print("\n--- TASKS ---")
   for task in tasks:
       print(task)
