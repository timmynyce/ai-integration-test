def improve_structured_prd(prd, feedback):
    prompt = f"""
Return ONLY valid JSON.
Do not include markdown.
Do not include explanation text.
Do not wrap the JSON in triple backticks.

Keep exactly this structure:

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

Fix these issues:
{json.dumps(feedback, indent=2)}

Current PRD:
{json.dumps(prd, indent=2)}

Rules:
- Preserve meaning
- Improve structure only where needed
- Return one valid JSON object only
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1800,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1

    if start == -1 or end == 0:
        raise ValueError("Model did not return a JSON object.")

    json_text = raw[start:end]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("\n--- RAW MODEL OUTPUT ---\n")
        print(raw)
        print("\n--- EXTRACTED JSON TEXT ---\n")
        print(json_text)
        raise ValueError(f"Model returned invalid JSON: {e}")