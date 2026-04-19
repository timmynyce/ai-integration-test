import os  # access environment variables
import numpy as np  # used for similarity math
from dotenv import load_dotenv  # load .env file
from openai import OpenAI  # OpenAI API client

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client using API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read the sample document from file
with open("sample_doc.txt", "r", encoding="utf-8") as file:
    document_text = file.read()


def chunk_text(text, chunk_size=250):
    # Simple character-based chunking
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


def get_embedding(text):
    # Create embedding using OpenAI embeddings API
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    # Measures similarity between two vectors
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def generate_answer(question, context):
    # Ask the LLM to answer using only retrieved context
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Answer the user's question using only the provided context. If the answer is not in the context, say you do not have enough information."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    )
    return response.choices[0].message.content


chunks = chunk_text(document_text)

chunk_store = []

for i, chunk in enumerate(chunks):
    embedding = get_embedding(chunk)

    chunk_store.append({
        "chunk_id": i + 1,
        "text": chunk,
        "embedding": embedding
    })

# Ask user for a question
user_question = input("Enter a question about the document: ")

# Embed the question
question_embedding = get_embedding(user_question)

# Score each chunk against the question
scored_chunks = []

for item in chunk_store:
    score = cosine_similarity(question_embedding, item["embedding"])
    scored_chunks.append({
        "chunk_id": item["chunk_id"],
        "text": item["text"],
        "score": score
    })

# Sort by highest similarity
scored_chunks.sort(key=lambda x: x["score"], reverse=True)

# Keep top 2 chunks
top_chunks = scored_chunks[:2]

print("\nTop Matching Chunks:\n")

for result in top_chunks:
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Similarity Score: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print("-" * 50)

# Combine retrieved chunks into one context block
context = "\n\n".join([item["text"] for item in top_chunks])

# Generate final grounded answer
final_answer = generate_answer(user_question, context)

print("\nFinal RAG Answer:\n")
print(final_answer)
