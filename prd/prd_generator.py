import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-haiku-4-5-20251001"

def convert_prd_to_json(prd_text):
    prompt = f"""
Return ONLY valid JSON.
Do not include markdown.
Do not include explanation text.
Do not wrap the JSON in triple backticks.

Use exactly this structure:

{{
  "product_name": "string",
  "user_types": ["string"],
  "features": [
    {{
      "name": "string",
      "requirements": ["string"]
    }}
  ],
  "success_metrics": ["string"],
  "constraints": ["string"],
  "edge_cases": ["string"]
}}

Rules:
- Extract from the PRD faithfully
- Do not invent major new functionality
- Keep the output compact
- Limit features to the 8 most important feature groups
- Limit each feature to at most 6 requirements
- Limit success_metrics to at most 8 items
- Limit constraints to at most 6 items
- Limit edge_cases to at most 8 items
- Every value must be valid JSON
- Escape quotes properly
- Return one complete JSON object only

PRD:
{prd_text}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2200,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1

    if start == -1 or end == 0:
        print("\n--- RAW MODEL OUTPUT ---\n")
        print(raw)
        raise ValueError("Model did not return a complete JSON object.")

    json_text = raw[start:end]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("\n--- RAW MODEL OUTPUT ---\n")
        print(raw)
        print("\n--- EXTRACTED JSON TEXT ---\n")
        print(json_text)
        raise ValueError(f"Model returned invalid JSON: {e}")