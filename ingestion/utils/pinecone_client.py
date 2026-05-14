import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

_index = None

def get_index():
    global _index
    if _index:
        return _index

    api_key = os.getenv("PINECONE_API_KEY")
    name    = os.getenv("PINECONE_INDEX_NAME")

    if not api_key or not name:
        raise ValueError("PINECONE_API_KEY and PINECONE_INDEX_NAME must be set in .env")

    pc = Pinecone(api_key=api_key)

    if name not in pc.list_indexes().names():
        print(f"Creating Pinecone index '{name}'...")
        pc.create_index(
            name=name,
            dimension=1024,          # matches intfloat/multilingual-e5-large
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("Index created.")
    else:
        print(f"Index '{name}' already exists.")

    _index = pc.Index(name)
    return _index