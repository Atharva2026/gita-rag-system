import re


def clean_text(text: str) -> str:
    """
    Remove common noise from lecture transcript PDFs:
    - Page numbers like 'Page 3' or '- 3 -'
    - Excessive blank lines
    - Extra whitespace and tabs
    """
    # Remove page number patterns
    text = re.sub(r'\bPage\s+\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'-\s*\d+\s*-', '', text)

    # Collapse 3+ blank lines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse multiple spaces/tabs into one space
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()