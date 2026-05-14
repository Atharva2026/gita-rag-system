from utils.pinecone_client import get_index

BATCH_SIZE = 100   # Pinecone recommends max 100 vectors per upsert call


def is_already_uploaded(index, file_stem: str) -> bool:
    """Check if the first chunk of this file already exists in Pinecone."""
    try:
        result = index.fetch(ids=[f"{file_stem}_chunk_0"])
        return bool(result.vectors)
    except Exception:
        return False


def upload_batch(chunks: list[dict], file_stem: str):
    """
    Upserts all chunks for one PDF into Pinecone.
    Skips files that are already uploaded (safe to re-run the pipeline).
    """
    index = get_index()

    if is_already_uploaded(index, file_stem):
        print(f"  Already in Pinecone — skipping")
        return

    total = len(chunks)
    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]

        vectors = [
            {
                "id":       f"{file_stem}_chunk_{c['metadata']['chunk_index']}",
                "values":   c["embedding"],
                "metadata": c["metadata"],
            }
            for c in batch
        ]

        index.upsert(vectors=vectors)
        print(f"  Uploaded {min(i + BATCH_SIZE, total)}/{total} chunks", end="\r")

    print(f"  Done — {total} chunks uploaded          ")