import requests
import os


def post_json(url: str, payload: dict, timeout_seconds: int = 10):
   try:
       response = requests.post(url, json=payload, timeout=timeout_seconds)

       try:
           body = response.json()
       except ValueError:
           body = {"raw_text": response.text}

       return response.status_code, body

   except requests.RequestException as e:
       return 0, {"error": str(e)}


# IMPORTANT:
# Keep this function in the same file so Part 2 ADDS to Part 1
# instead of overwriting Part 1 logic.
def post_github_issue(url: str, payload: dict):
   token = os.getenv("GITHUB_TOKEN")

   if not token:
       return 0, {"error": "Missing GITHUB_TOKEN"}

   headers = {
       "Authorization": f"Bearer {token}",
       "Accept": "application/vnd.github+json"
   }

   try:
       response = requests.post(url, json=payload, headers=headers)

       try:
           body = response.json()
       except ValueError:
           body = {"raw_text": response.text}

       return response.status_code, body

   except requests.RequestException as e:
       return 0, {"error": str(e)}
