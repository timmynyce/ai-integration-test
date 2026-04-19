def classify_task(criterion: str) -> str:
   c = criterion.lower()

   if any(word in c for word in ["stripe", "api", "integration", "email delivery", "connect"]):
       return "integration"

   if any(word in c for word in ["display", "view", "dashboard", "interface", "mobile-friendly", "show"]):
       return "frontend"

   if any(word in c for word in ["validate", "block", "prevent", "enforce", "require"]):
       return "validation"

   if any(word in c for word in ["store", "track", "log", "retain", "audit", "data", "status"]):
       return "data"

   if any(word in c for word in ["process", "generate", "trigger", "assign", "release", "hold", "retry"]):
       return "backend"

   return "general"

def criterion_to_task_text(criterion: str) -> str:
   c = criterion.strip()

   replacements = [
       ("System supports: ", ""),
       ("Organizer can ", "Build organizer capability to "),
       ("System prevents ", "Implement rule to prevent "),
       ("System displays ", "Display "),
       ("System blocks ", "Implement logic to block "),
       ("System logs ", "Log "),
       ("System stores ", "Store "),
   ]

   for old, new in replacements:
       if c.startswith(old):
           return c.replace(old, new, 1)

   return c

def generate_tasks(stories):
   tasks = []

   for story_obj in stories:
       feature = story_obj["feature"]
       story = story_obj["story"]
       actor = story_obj.get("actor", "User")

       for criterion in story_obj.get("acceptance_criteria", []):
           task_text = criterion_to_task_text(criterion)
           task_type = classify_task(criterion)

           tasks.append({
               "feature": feature,
               "story": story,
               "actor": actor,
               "task_type": task_type,
               "task": task_text,
               "source_acceptance_criterion": criterion
           })

   return tasks
