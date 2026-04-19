def improve_tasks(tasks):
   improved = []

   replacements = [
       ("use ", "implement "),
       ("handle ", "implement handling for "),
       ("manage ", "build management flow for "),
       ("support ", "implement support for ")
   ]

   for task_obj in tasks:
       new_task = dict(task_obj)
       text = new_task["task"]

       lowered = text.lower()
       for old, new in replacements:
           if lowered.startswith(old):
               text = new.lower() + text[len(old):]
               break

       new_task["task"] = text
       improved.append(new_task)

   return improved
