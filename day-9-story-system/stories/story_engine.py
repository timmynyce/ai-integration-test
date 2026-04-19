import json
import os
from datetime import datetime

PRD_PATH = "prd/versions/prd_20260412_120028.json"

def load_prd(path):
   with open(path, "r", encoding="utf-8") as f:
       return json.load(f)

def save_stories(stories):
   os.makedirs("stories/versions", exist_ok=True)

   ts = datetime.now().strftime("%Y%m%d_%H%M%S")
   path = f"stories/versions/stories_{ts}.json"

   with open(path, "w", encoding="utf-8") as f:
       json.dump(stories, f, indent=2)

   return path

from story_generator import generate_stories
from story_validator import validate_stories

def build_stories():
   prd = load_prd(PRD_PATH)

   stories = generate_stories(prd)

   validation = validate_stories(stories)
   print("Validation:", validation)

   path = save_stories(stories)
   print("Saved stories to:", path)

   return stories

if __name__ == "__main__":
   stories = build_stories()

   print("\n--- STORIES ---")
   for s in stories:
       print(s)

