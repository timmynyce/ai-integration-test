def validate_tasks(tasks):
   errors = []

   valid_types = {"backend", "frontend", "integration", "validation", "data", "general"}

   for task_obj in tasks:
       task_text = task_obj.get("task", "").strip()
       task_type = task_obj.get("task_type", "").strip()

       if len(task_text) < 15:
           errors.append(f"Weak task text: {task_text}")

       vague_patterns = [
           "use ",
           "handle ",
           "manage ",
           "support ",
           "intended outcome"
       ]

       lowered = task_text.lower()
       for pattern in vague_patterns:
           if lowered.startswith(pattern):
               errors.append(f"Vague task wording: {task_text}")
               break

       if task_type not in valid_types:
           errors.append(f"Invalid task type: {task_type}")

       if not task_obj.get("feature"):
           errors.append(f"Missing feature on task: {task_text}")

       if not task_obj.get("source_acceptance_criterion"):
           errors.append(f"Missing source acceptance criterion on task: {task_text}")

   return {
       "valid": len(errors) == 0,
       "errors": errors
   }
