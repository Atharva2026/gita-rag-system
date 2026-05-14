from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(path: str) -> str:
    """
    Fallback for scanned PDFs where pdfplumber returns no text.
    Converts each page to an image and runs Tesseract OCR on it.

    Requirements:
        sudo apt install tesseract-ocr poppler-utils   (Linux)
        brew install tesseract poppler                  (Mac)
    """
    print("  Running OCR — this may take a few minutes...")
    images = convert_from_path(path, dpi=300)
    pages  = [pytesseract.image_to_string(img) for img in images]
    return "\n".join(pages)