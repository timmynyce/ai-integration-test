import os
import json
import chromadb
from dotenv import load_dotenv
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Validate API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
   raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

# Shared base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

# Anthropic model
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Initialize Anthropic client
anthropic_client = Anthropic(api_key=api_key)

# Initialize Chroma
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="documents")

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, top_k=3):
   query_embedding = embedding_model.encode(query).tolist()

   results = collection.query(
       query_embeddings=[query_embedding],
       n_results=top_k
   )

   documents = results.get("documents", [[]])[0]
   return "\n".join(documents)


def summarize_text(text):
   prompt = f"""Summarize the following clearly and simply.

Text:
{text}

Return a short summary.
"""

   response = anthropic_client.messages.create(
       model=CLAUDE_MODEL,
       max_tokens=200,
       temperature=0.3,
       messages=[
           {"role": "user", "content": prompt}
       ]
   )

   return response.content[0].text.strip()


def explain_text(text):
   prompt = f"""Explain the following in beginner-friendly language.

Text:
{text}

Use a simple explanation and a short example if helpful.
"""

   response = anthropic_client.messages.create(
       model=CLAUDE_MODEL,
       max_tokens=250,
       temperature=0.3,
       messages=[
           {"role": "user", "content": prompt}
       ]
   )

   return response.content[0].text.strip()

def compare_text(text):
    prompt = f"""Compare the concepts in the following text clearly.

Return these sections:
- Concept 1
- Concept 2
- Key Differences
- When to Use Each
- Simple Example

Be complete, specific, and beginner-friendly.

Text:
{text}
"""

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text.strip()

def decide_next_action(user_input, scratchpad):
    prompt = f"""You are a simple AI agent.

Your job is to decide the next best action.

You may choose exactly one of these actions:
- retrieve_context
- summarize_text
- explain_text
- compare_text
- final_answer

Rules:
- Use retrieve_context if external context from the vector database would help.
- Use summarize_text if the text should be condensed.
- Use explain_text if the text should be taught simply.
- Use compare_text if the request asks for differences between concepts.
- Use final_answer only when you have enough information to answer the user.

Return ONLY valid JSON.
Do not include markdown.
Do not include code fences.
Do not include explanation text before or after the JSON.

Return this exact structure:
{{
  "thought": "brief reasoning",
  "action": "one allowed action",
  "action_input": "the text or query for that action"
}}

Examples:

Example 1:
User request: What is semantic search?
Scratchpad so far:
The user is asking a knowledge question that likely benefits from retrieved context.
Output:
{{
  "thought": "I should retrieve relevant context before answering.",
  "action": "retrieve_context",
  "action_input": "What is semantic search?"
}}

Example 2:
User request: Explain embeddings in simple terms
Scratchpad so far:
The user wants a simple explanation, not a retrieval step.
Output:
{{
  "thought": "The user wants a beginner-friendly explanation.",
  "action": "explain_text",
  "action_input": "Explain embeddings in simple terms"
}}

Example 3:
User request: What is semantic search?
Scratchpad so far:
Step 1
Thought: I should retrieve relevant context before answering.
Action: retrieve_context
Action Input: What is semantic search?
Tool Result: Semantic search finds content based on meaning rather than exact keyword matching.
Output:
{{
  "thought": "I now have enough information to answer the user.",
  "action": "final_answer",
  "action_input": "Semantic search finds content based on meaning rather than exact keyword matching."
}}

User request:
{user_input}

Scratchpad so far:
{scratchpad}
"""

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=250,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.content[0].text.strip()

    print("\n--- Raw Agent Decision ---")
    print(raw_text)

    # Remove common markdown fences if they appear anyway
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(
            "Agent returned invalid JSON.\n"
            f"Raw response was:\n{raw_text}"
        )

def run_tool(action, action_input):
   if action == "retrieve_context":
       return retrieve_context(action_input)

   elif action == "summarize_text":
       return summarize_text(action_input)

   elif action == "explain_text":
       return explain_text(action_input)

   elif action == "compare_text":
       return compare_text(action_input)

   elif action == "final_answer":
       return action_input

   else:
       raise ValueError(f"Unknown action: {action}")

def run_agent(user_input, max_steps=5):
   scratchpad = ""
   step = 1

   while step <= max_steps:
       print(f"\n--- Agent Step {step} ---")

       decision = decide_next_action(user_input, scratchpad)
       thought = decision["thought"]
       action = decision["action"]
       action_input = decision["action_input"]

       print(f"Thought: {thought}")
       print(f"Action: {action}")
       print(f"Action Input: {action_input}")

       if action == "final_answer":
           print("\nAgent finished.")
           return action_input

       tool_result = run_tool(action, action_input)

       print("\nTool Result:")
       print(tool_result)

       scratchpad += f"""
Step {step}
Thought: {thought}
Action: {action}
Action Input: {action_input}
Tool Result: {tool_result}
"""

       step += 1

return f"""Agent stopped after reaching the maximum step limit ({max_steps} steps).

The request may require more steps than allowed or clearer instructions.

Suggestions:
- Try simplifying the request
- Be more specific about the desired outcome
- Break the task into smaller parts

Original request:
{user_input}
"""

def run_fixed_workflow(user_input):
   lowered = user_input.lower()

   if "summarize" in lowered:
       print("Workflow path: summarize")
       return summarize_text(user_input)

   elif "explain" in lowered:
       print("Workflow path: explain")
       return explain_text(user_input)

   else:
       print("Workflow path: retrieve + answer")
       context = retrieve_context(user_input)

       prompt = f"""Answer the user's question using the context below.

Context:
{context}

Question:
{user_input}

Answer clearly and directly.
"""

       response = anthropic_client.messages.create(
           model=CLAUDE_MODEL,
           max_tokens=300,
           temperature=0.3,
           messages=[
               {"role": "user", "content": prompt}
           ]
       )

       return response.content[0].text.strip()

print("Agent system initialized.")
print("Tools ready.")
print("Decision function ready.")
print("Tool executor ready.")
print("Agent loop ready.")
print("Workflow baseline ready.")

while True:
   mode = input("\nChoose mode ('workflow', 'agent', or 'exit'): ").strip().lower()

   if mode == "exit":
       print("Exiting Day 6 system.")
       break

   if mode not in ["workflow", "agent"]:
       print("Invalid mode. Choose 'workflow', 'agent', or 'exit'.")
       continue

   user_input = input("\nEnter your request: ").strip()

   if mode == "workflow":
       result = run_fixed_workflow(user_input)
       print("\nWorkflow Result:")
       print(result)

   elif mode == "agent":
       result = run_agent(user_input)
       print("\nAgent Result:")
       print(result)
