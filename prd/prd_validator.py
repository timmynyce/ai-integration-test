def validate_structured_prd(prd):
   errors = []

   if len(prd.get("features", [])) == 0:
       errors.append("No features extracted")

   if len(prd.get("success_metrics", [])) == 0:
       errors.append("Missing success metrics")

   for f in prd.get("features", []):
       if len(f.get("requirements", [])) < 2:
           errors.append(f"Weak feature: {f.get('name')}")

   return {
       "valid": len(errors) == 0,
       "errors": errors
   }
