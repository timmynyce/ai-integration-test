def validate_stories(stories):
   errors = []

   for s in stories:
       if not s.get("actor"):
           errors.append(f"Missing actor for feature {s['feature']}")

       if len(s.get("acceptance_criteria", [])) < 2:
           errors.append(f"Weak acceptance criteria for {s['feature']}")

       if "user" in s["story"].lower():
           errors.append(f"Generic actor used in {s['feature']}")

   return {
       "valid": len(errors) == 0,
       "errors": errors
   }
