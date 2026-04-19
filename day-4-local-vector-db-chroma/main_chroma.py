# Standard library imports
import os

# Third-party imports
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Initialize clients
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="documents")
print("Collection count at startup:", collection.count())

model = SentenceTransformer("all-MiniLM-L6-v2")

anthropic_client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

print("Chroma initialized.")

documents = [
    "QUEST is a white-label platform for memberships, events, and fundraising.",
    "Users can create challenges, join programs, and track progress.",
    "Admins can manage users, run reports, and configure the system."
]

embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[f"id{i}" for i in range(len(documents))]
)

print("Documents stored.")
print("Collection count after add:", collection.count())

while True:
    query = input("\nAsk a question (or type 'exit'): ")

    if query.lower() == "exit":
        break

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    retrieved_docs = results["documents"][0]

    print("\nRetrieved Context:\n")
    for doc in retrieved_docs:
        print("-", doc)

    context = "\n- ".join(retrieved_docs)
    context = "- " + context

    prompt = f"""
You are an assistant.

Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.content[0].text

    print("\nFinal Answer:\n")
    print(answer)