from sentence_transformers import SentenceTransformer

# Load a local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "QUEST helps organizations manage memberships and events.",
    "A dog is running in the park."
]

embeddings = model.encode(texts)

print("Local embeddings created successfully.\n")

for i, embedding in enumerate(embeddings):
    print(f"Text {i + 1}: {texts[i]}")
    print(f"Embedding length: {len(embedding)}")
    print("-" * 50)
