def validate_integration_input(record: dict) -> dict:
   issues = []

   required_fields = [
       "task",
       "integration_target",
       "payload",
       "response_status",
       "response_body"
   ]

   for field in required_fields:
       if field not in record:
           issues.append(f"Missing required field: {field}")

   if "task" in record and not record["task"]:
       issues.append("Task is empty")

   if "integration_target" in record:
       allowed_targets = [
           "https://httpbin.org/post"
       ]

       if not (
           record["integration_target"] in allowed_targets
           or "api.github.com/repos/" in record["integration_target"]
       ):
           issues.append("Integration target is not approved")

   if "payload" in record and not isinstance(record["payload"], dict):
       issues.append("Payload is not a dictionary")

   return {
       "valid": len(issues) == 0,
       "issues": issues
   }
