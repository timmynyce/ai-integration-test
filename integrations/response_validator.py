def validate_integration_response(status_code: int, response_body: dict) -> dict:
   issues = []

   if status_code == 0:
       issues.append("Request failed before receiving an HTTP response")

   if status_code >= 400:
       issues.append(f"HTTP error status returned: {status_code}")

   if not isinstance(response_body, dict):
       issues.append("Response body is not a dictionary")

   if "error" in response_body:
       issues.append(f"Integration client error: {response_body['error']}")

   return {
       "valid": len(issues) == 0,
       "issues": issues
   }
