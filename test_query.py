"""
BhaktiSetu — Query Test Script
================================
Run this in your IDE after ingestion to verify that retrieval is working.
No backend or frontend needed — just Python.

Usage:
    cd bhaktisetu
    python test_query.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent / "ingestion"))

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


# ── Config ────────────────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.72   # below this = answer not found
TOP_K                = 5      # how many chunks to retrieve


# ── Load model and index ──────────────────────────────────────────────────────
print("Loading model...")
model = SentenceTransformer("intfloat/multilingual-e5-large")

index = Pinecone(api_key=os.getenv("PINECONE_API_KEY")).Index(
    os.getenv("PINECONE_INDEX_NAME")
)
print("Ready. Type your question below.\n")


# ── Query function ────────────────────────────────────────────────────────────
def ask(question: str):
    print(f"\nQuestion: {question}")
    print("-" * 60)

    vec     = model.encode([question], normalize_embeddings=True)[0].tolist()
    results = index.query(vector=vec, top_k=TOP_K, include_metadata=True)

    if not results.matches:
        print("No results returned from Pinecone.")
        return

    top_score = results.matches[0].score

    if top_score < CONFIDENCE_THRESHOLD:
        print(f"Low confidence ({top_score:.3f}) — not found in lectures.")
        return

    for i, match in enumerate(results.matches):
        m = match.metadata
        print(f"\n[Result {i+1}]  Score: {match.score:.3f}")
        print(f"  Source   : {m.get('source_file', 'unknown')}")
        print(f"  Speaker  : {m.get('speaker', 'unknown')}")
        print(f"  Segment  : {m.get('segment_type', 'unknown')}")
        ref = m.get('scripture_ref', '')
        if ref:
            print(f"  Ref      : {ref}")
        print(f"  Text     : {m.get('text', '')[:400]}...")


# ── Interactive loop ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Test with a few sample questions first
    sample_questions = [
        "What does Srila Prabhupada say about false pride?",
        "What is the story of Madhavendra Puri and the kheer?",
        "How should we overcome material attachment?",
    ]

    print("Running sample questions to verify retrieval...\n")
    for q in sample_questions:
        ask(q)

    print("\n" + "=" * 60)
    print("Sample questions done. Now enter your own questions.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Your question: ").strip()
        if user_input.lower() in ("exit", "quit", "q"):
            break
        if user_input:
            ask(user_input)