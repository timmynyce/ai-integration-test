def build_task_payload(task_obj: dict) -> dict:
   return {
       "title": task_obj["task"],
       "feature": task_obj["feature"],
       "story": task_obj["story"],
       "actor": task_obj["actor"],
       "task_type": task_obj["task_type"],
       "source_acceptance_criterion": task_obj["source_acceptance_criterion"]
   }

def build_github_issue_payload(task_obj: dict) -> dict:
   return {
       "title": task_obj["task"],
       "body": f"""
Feature: {task_obj['feature']}
Story: {task_obj['story']}
Actor: {task_obj['actor']}
Task Type: {task_obj['task_type']}
""",
       "labels": ["ai-generated", task_obj["task_type"]]
   }

