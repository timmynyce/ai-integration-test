def apply_output_guardrails(record: dict) -> dict:
   issues = []

   response_status = record.get("response_status", 0)
   response_body = record.get("response_body", {})
   payload = record.get("payload", {})
   integration_target = record.get("integration_target", "")

   if response_status == 0:
       issues.append("No HTTP response received")

   if response_status >= 400:
       issues.append(f"HTTP error response: {response_status}")

   if not isinstance(response_body, dict):
       issues.append("Response body is not structured as a dictionary")

   if integration_target.endswith("/issues"):
       if "title" not in payload or not payload.get("title"):
           issues.append("GitHub issue payload missing title")

   if isinstance(response_body, dict) and "error" in response_body:
       issues.append(f"Response body contains error: {response_body['error']}")

   return {
       "valid": len(issues) == 0,
       "issues": issues
   }
