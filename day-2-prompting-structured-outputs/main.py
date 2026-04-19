import os  # access environment variables (API keys)
import json  # parse and format JSON output
from dotenv import load_dotenv  # load variables from .env file
import anthropic  # Anthropic API client

# Load environment variables from .env into the app
load_dotenv()

# Initialize Anthropic client using API key (keeps key out of code)
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Get dynamic input from user instead of hardcoding prompt
user_input = input("Enter a product idea or PRD text: ")

# Structured prompt
# We are forcing the model to return a predictable structure
# so the output can be used in downstream workflows
prompt = f"""
You are a product analyst.

Convert the following input into valid JSON.

Rules:
- Return JSON only
- Do not include markdown
- Do not include explanation text
- Use exactly these keys:
  - title
  - summary
  - user_stories

For user_stories:
- Return an array
- Each item must include:
  - id
  - story

Input:
{user_input}
"""

def call_anthropic():
    # Send structured prompt to model and receive response
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",  # fast, cost-efficient model for structured tasks
        max_tokens=500,  # limit response size
        temperature=0.2,  # low = more consistent, predictable output
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract only the text portion of the response
    return response.content[0].text


def clean_json_text(text):
    # Remove leading/trailing whitespace
    cleaned = text.strip()

    # Remove markdown code fences if the model included them anyway
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").strip()

    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()

    return cleaned


def validate_output(data):
    # Validate top-level structure
    required_top_level_keys = ["title", "summary", "user_stories"]

    for key in required_top_level_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    # Validate expected types
    if not isinstance(data["title"], str):
        raise ValueError("title must be a string")

    if not isinstance(data["summary"], str):
        raise ValueError("summary must be a string")

    if not isinstance(data["user_stories"], list):
        raise ValueError("user_stories must be a list")

    # Validate each story object
    for i, story in enumerate(data["user_stories"]):
        if not isinstance(story, dict):
            raise ValueError(f"user_stories[{i}] must be an object")

        if "id" not in story:
            raise ValueError(f"user_stories[{i}] is missing 'id'")

        if "story" not in story:
            raise ValueError(f"user_stories[{i}] is missing 'story'")

        if not isinstance(story["id"], str):
            raise ValueError(f"user_stories[{i}]['id'] must be a string")

        if not isinstance(story["story"], str):
            raise ValueError(f"user_stories[{i}]['story'] must be a string")


if __name__ == "__main__":
    try:
        # Step 1: Call model and capture raw output
        raw_output = call_anthropic()

        print("\nRaw Model Output:\n")
        print(raw_output)

        # Debug view helps reveal hidden characters if parsing fails
        print("\nDebug Raw Output (repr):\n")
        print(repr(raw_output))

        # Step 2: Clean output before parsing
        cleaned_output = clean_json_text(raw_output)

        print("\nCleaned Output:\n")
        print(cleaned_output)

        # Step 3: Parse JSON
        parsed_output = json.loads(cleaned_output)

        # Step 4: Validate structure and types
        validate_output(parsed_output)

        # Step 5: Pretty-print validated result
        print("\nValidated JSON Output:\n")
        print(json.dumps(parsed_output, indent=2))

    except json.JSONDecodeError as e:
        print("\nError: Model output was not valid JSON.")
        print(f"Details: {e}")

    except ValueError as e:
        print(f"\nValidation Error: {e}")

    except Exception as e:
        print(f"\nUnexpected Error: {e}")

