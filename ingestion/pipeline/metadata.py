import re
from pathlib import Path


# Words/phrases that indicate a Q&A section rather than main lecture body.
# Identified from real ISKCON transcript samples.
QA_SIGNALS = [
    "can you hear",
    "my question is",
    "hare krishna prabhu",
    "dandadat pranam",
    "thank you prabhuji",
    "mataji",
    "prabhuji please",
    "i have a question",
    "unmute and please ask",
]

# Regex patterns to detect scripture references in text
SCRIPTURE_PATTERNS = [
    r'\bSB\s+\d+\.\d+\.\d+\b',                        # SB 5.12.2  (must have all 3 numbers)
    r'\bSB\s+\d+\.\d+\b',                              # SB 5.12
    r'\bBhagavatam\s+\d+(?:th|nd|rd|st)\s+canto\b',   # Bhagavatam 5th canto
    r'\bGita\s+\d+\.\d+\b',                            # Gita 7.15
    r'\bcanto\s+\d+\s+chapter\s+\d+\s+text\s+\d+\b',  # canto 5 chapter 12 text 2
]


def detect_segment(text: str) -> str:
    """Returns 'qa_session' or 'lecture_body' based on text content."""
    tl = text.lower()
    return "qa_session" if any(s in tl for s in QA_SIGNALS) else "lecture_body"


def extract_scripture_ref(text: str) -> str:
    """Returns the first scripture reference found, or empty string."""
    for pattern in SCRIPTURE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return ""


def extract_speaker(stem: str) -> str:
    # Try double underscore first (preferred format)
    if "__" in stem:
        return stem.split("__")[-1].replace("_", " ").strip()

    # Fallback: last segment after two or more spaces
    import re
    parts = re.split(r'\s{2,}', stem)
    if len(parts) > 1:
        return parts[-1].strip()

    return "Unknown"


def build_metadata(chunks: list[dict], pdf_path: Path) -> list[dict]:
    """
    Attaches a metadata dict to each chunk.
    This metadata is stored in Pinecone alongside the vector
    and returned with every search result.
    """
    speaker = extract_speaker(pdf_path.stem)

    for i, chunk in enumerate(chunks):
        chunk["metadata"] = {
            "source_file":   pdf_path.stem,
            "chunk_index":   i,
            "text":          chunk["orig"],      # original text — shown to users
            "speaker":       speaker,
            "segment_type":  detect_segment(chunk["orig"]),
            "scripture_ref": extract_scripture_ref(chunk["orig"]),
        }

    return chunks