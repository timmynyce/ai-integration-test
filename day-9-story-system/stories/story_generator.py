def infer_actor(feature_name):
    name = feature_name.lower()

    if "payment" in name or "payout" in name:
        return "Organizer"

    if "refund" in name or "dispute" in name:
        return "Organizer"

    if "ticket" in name or "delivery" in name:
        return "Attendee"

    if "discovery" in name or "search" in name:
        return "Attendee"

    if "moderation" in name or "content policy" in name:
        return "Admin"

    if "admin" in name:
        return "Admin"

    if "organizer" in name or "event" in name:
        return "Organizer"

    if "attendee" in name:
        return "Attendee"

    return "User"

def generate_stories(prd):
   stories = []

   for feature in prd.get("features", []):
       feature_name = feature["name"]
       requirements = feature.get("requirements", [])

       actor = infer_actor(feature_name)

       story_text = f"As an {actor.lower()}, I want to use {feature_name} so that I can achieve its intended outcome"

       acceptance = []

       for req in requirements:
           acceptance.append(f"System supports: {req}")

       stories.append({
           "actor": actor,
           "feature": feature_name,
           "story": story_text,
           "acceptance_criteria": acceptance
       })

   return stories
