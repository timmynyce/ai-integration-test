def review_code(code_obj: dict) -> dict:
   issues = []

   code = code_obj.get("code", "")
   task = code_obj.get("task", "")

   if "not_implemented" in code:
       issues.append("Code still contains placeholder implementation")

   if len(code.strip()) < 80:
       issues.append("Code output is too short to be meaningful")

   if task and task.lower() not in code.lower():
       issues.append("Task context is weakly reflected in code")

   if "return True" in code:
       issues.append("Validation logic may be too shallow")

   valid = len(issues) == 0

   return {
       "valid": valid,
       "issues": issues
   }
