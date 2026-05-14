from langchain_text_splitters import RecursiveCharacterTextSplitter

# 800 tokens with 150 overlap because ISKCON lecture transcripts contain
# long contextual stories (Madhavendra Puri, Parikshit-Sringi, etc.)
# that span multiple pages. Smaller chunks lose the narrative context.
# \u0964 is the Devanagari danda (।) — a sentence boundary in Sanskrit text.

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", "\u0964 ", ". ", " "],
)


def chunk_text(normalized: str, original: str) -> list[dict]:
    """
    Splits both the normalized text (used for embedding) and the
    original text (shown to users) into aligned chunks.

    Returns a list of dicts: [{"norm": ..., "orig": ...}, ...]
    """
    norm_chunks = _splitter.split_text(normalized)
    orig_chunks = _splitter.split_text(original)

    # Take the minimum in the rare case counts differ
    n = min(len(norm_chunks), len(orig_chunks))

    return [
        {"norm": norm_chunks[i], "orig": orig_chunks[i]}
        for i in range(n)
    ]