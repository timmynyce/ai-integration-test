import chromadb
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Validate API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

# Anthropic model
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Initialize Anthropic client
anthropic_client = Anthropic(api_key=api_key)

# Initialize Chroma
client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory="./chroma_db"
    )
)

collection = client.get_or_create_collection(name="documents")

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, top_k=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]

def classify_intent(user_input):
   prompt = f"""Classify the user request into exactly one of these categories:
question
summarize
explain
prd

Return only one word.

Use prd for requests that describe building a product, system, feature, platform, or app.

Examples:
What is vector similarity? -> question
Summarize this paragraph -> summarize
Explain embeddings simply -> explain
Build a platform for events and payments -> prd

User input:
{user_input}
"""

   response = anthropic_client.messages.create(
       model="claude-haiku-4-5-20251001",
       max_tokens=10,
       temperature=0,
       messages=[
           {"role": "user", "content": prompt}
       ]
   )

   return response.content[0].text.strip().lower()

def handle_question(user_input):
    context_docs = retrieve_context(user_input, top_k=3)
    context_text = "\n".join(context_docs)

    prompt = f"""Answer the user's question using the context below.

Context:
{context_text}

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

def handle_summarize(user_input):
    prompt = f"""Summarize the following clearly and simply.

Text:
{user_input}

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

def handle_explain(user_input):
    prompt = f"""Explain the following in beginner-friendly language.

Request:
{user_input}

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

def run_workflow(user_input):
   intent = classify_intent(user_input)
   print(f"Detected intent: {intent}")

   if intent == "question":
       print("Path taken: question handler")
       return handle_question(user_input)

   elif intent == "summarize":
       print("Path taken: summarize handler")
       return handle_summarize(user_input)

   elif intent == "explain":
       print("Path taken: explain handler")
       return handle_explain(user_input)

   elif intent == "prd":
       print("Path taken: PRD workflow handler")
       return handle_prd_workflow(user_input)

   else:
       return "Could not determine request type."

def handle_prd_workflow(user_input):
    print("Step 1: Structuring PRD")

    step1_prompt = f"""Convert the following input into a structured PRD with these sections:
- Overview
- Goals
- Features
- Requirements
- Constraints
- Success Metrics

Be clear, organized, and specific.
If the user input is vague, make reasonable assumptions and keep them practical.

Input:
{user_input}
"""

    step1_response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=400,
        temperature=0.3,
        messages=[
            {"role": "user", "content": step1_prompt}
        ]
    )

    structured_prd = step1_response.content[0].text.strip()
    print("\n--- Step 1 Output ---")
    print(structured_prd)

    print("\nStep 2: Refining PRD")

    step2_prompt = f"""Improve and refine the following PRD.
Make it clearer, more complete, and better organized.

PRD:
{structured_prd}
"""

    step2_response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=400,
        temperature=0.3,
        messages=[
            {"role": "user", "content": step2_prompt}
        ]
    )

    refined_prd = step2_response.content[0].text.strip()
    print("\n--- Step 2 Output ---")
    print(refined_prd)

    print("\nStep 3: Final Output")

    step3_prompt = f"""Turn this PRD into a clean final version ready to share.
Make the formatting clear and professional.
Do not repeat content unnecessarily.

PRD:
{refined_prd}
"""

    step3_response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        temperature=0.3,
        messages=[
            {"role": "user", "content": step3_prompt}
        ]
    )

    final_output = step3_response.content[0].text.strip()
    print("\n--- Step 3 Output ---")
    print(final_output)

    # Step 4 - Validation
    step4_prompt = f"""Check whether the following PRD is complete.

PRD:
{final_output}

Tasks:
1. Identify any missing sections or important details
2. Point out weak or vague areas
3. Suggest specific improvements

Be concise and practical.
"""

    step4_response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        temperature=0.3,
        messages=[
            {"role": "user", "content": step4_prompt}
        ]
    )

    validation_output = step4_response.content[0].text.strip()

    print("\n--- Step 4 Validation ---")
    print(validation_output)

    return f"""FINAL PRD:
{final_output}

VALIDATION:
{validation_output}
"""

print("Workflow system initialized.")
print("Retrieval function ready.")
print("Intent classifier ready.")
print("Question handler ready.")
print("Summarize handler ready.")
print("Explain handler ready.")
print("Workflow router ready.")
print("PRD workflow handler ready.")

while True:
    user_input = input("\nEnter your request (or type 'exit'): ")

    if user_input.lower() == "exit":
        print("Exiting workflow.")
        break

    result = run_workflow(user_input)
    print("\nResponse:")
    print(result)