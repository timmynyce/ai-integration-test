from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
   raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

client = Anthropic(api_key=api_key)

response = client.messages.create(
   model="claude-haiku-4-5-20251001",
   max_tokens=20,
   messages=[
       {"role": "user", "content": "Say setup is complete"}
   ]
)

print(response.content[0].text)
