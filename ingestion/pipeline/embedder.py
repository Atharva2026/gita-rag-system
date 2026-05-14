from sentence_transformers import SentenceTransformer

# multilingual-e5-large chosen over bge-large-en-v1.5 because ISKCON transcripts
# contain Sanskrit (romanized), Hindi, and English mixed in the same paragraph.
# This model handles all three without quality loss.
# First run will download ~2GB — subsequent runs use the local cache.

print("Loading embedding model (first run downloads ~2GB)...")
_model = SentenceTransformer("intfloat/multilingual-e5-large")
print("Model ready.")


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Generates a 1024-dimensional vector for each chunk.
    Uses the normalized text for embedding (better semantic matching).
    Original text is preserved in metadata for display.
    """
    texts      = [c["norm"] for c in chunks]
    embeddings = _model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,   # required for cosine similarity
    )

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    return chunks