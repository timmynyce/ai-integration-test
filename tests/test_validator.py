def validate_tests(tests):
   errors = []

   for t in tests:
       code = t["test_code"]

       if "assert" not in code:
           errors.append("Missing assert in test")

       if len(code) < 40:
           errors.append("Test too short")

   return {
       "valid": len(errors) == 0,
       "errors": errors
   }
