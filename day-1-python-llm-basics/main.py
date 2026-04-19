import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Prompt
#prompt = "Explain what a PRD is in 2 sentences."
#prompt = "Turn this idea into a simple product concept: a platform that helps kids build daily habits through challenges."
user_input = input("Enter your prompt: ")
prompt = user_input


# OpenAI call
def call_openai():
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# Anthropic call
def call_anthropic():
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    print("OpenAI Response:\n")
    # print(call_openai())

    print("\n------------------\n")

    print("Anthropic Response:\n")
    print(call_anthropic())