import pdfplumber
from utils.ocr_fallback import ocr_pdf


def parse_pdf(path: str) -> str:
    """
    Extract raw text from a PDF.
    Uses pdfplumber first. If average characters per page is too low
    (i.e. the PDF is a scanned image), falls back to OCR.
    """
    text  = ""
    pages = 0

    with pdfplumber.open(path) as pdf:
        pages = len(pdf.pages)
        for page in pdf.pages:
            t = page.extract_text(x_tolerance=2, y_tolerance=3)
            if t:
                text += t + "\n"

    avg_chars_per_page = len(text) / max(1, pages)

    if avg_chars_per_page < 50:
        print(f"  Low text yield ({avg_chars_per_page:.0f} chars/page) — switching to OCR")
        text = ocr_pdf(path)

    return text