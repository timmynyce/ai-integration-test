def slugify_task_name(task_text: str) -> str:
   cleaned = task_text.lower()
   for ch in [",", ".", ":", ";", "(", ")", "/", "-", "'"]:
       cleaned = cleaned.replace(ch, " ")
   parts = [p for p in cleaned.split() if p]
   return "_".join(parts[:8])


def generate_python_function_name(task_obj: dict) -> str:
   base = slugify_task_name(task_obj["task"])
   return f"task_{base}"


def generate_code(task_obj: dict) -> str:
   function_name = generate_python_function_name(task_obj)
   task_type = task_obj.get("task_type", "general")
   task_text = task_obj["task"]

   if task_type == "validation":
       return f'''def {function_name}(input_data: dict) -> bool:
   """
   Task: {task_text}
   """
   if not isinstance(input_data, dict):
       return False

   return True
'''

   if task_type == "integration":
       return f'''def {function_name}(payload: dict) -> dict:
   """
   Task: {task_text}
   """
   response = {{
       "status": "not_implemented",
       "task": "{task_text}"
   }}
   return response
'''

   if task_type == "data":
       return f'''def {function_name}(record: dict) -> dict:
   """
   Task: {task_text}
   """
   stored_record = dict(record)
   stored_record["processed"] = True
   return stored_record
'''

   if task_type == "frontend":
       return f'''def {function_name}(data: dict) -> dict:
   """
   Task: {task_text}
   """
   return {{
       "view_state": "ready",
       "data": data
   }}
'''

   return f'''def {function_name}() -> dict:
   """
   Task: {task_text}
   """
   return {{
       "status": "not_implemented",
       "task": "{task_text}"
   }}
'''
def generate_code_objects(tasks):
   code_objects = []

   for task_obj in tasks:
       code_objects.append({
           "feature": task_obj["feature"],
           "story": task_obj["story"],
           "actor": task_obj["actor"],
           "task_type": task_obj["task_type"],
           "task": task_obj["task"],
           "source_acceptance_criterion": task_obj["source_acceptance_criterion"],
           "code": generate_code(task_obj),
           "review": {
               "valid": False,
               "issues": []
           }
       })

   return code_objects
