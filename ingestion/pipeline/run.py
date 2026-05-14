"""
BhaktiSetu — Phase 1 Ingestion Pipeline
========================================
Run this once to process all PDFs and upload them to Pinecone.
Safe to re-run — already-uploaded files are automatically skipped.

Usage:
    cd bhaktisetu
    python ingestion/pipeline/run.py

    # Or for a specific folder:
    python ingestion/pipeline/run.py --folder /path/to/pdfs
"""

import sys
import argparse
from pathlib import Path

# Make ingestion/ importable regardless of where you run from
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.parser     import parse_pdf
from pipeline.cleaner    import clean_text
from pipeline.normalizer import normalize_text
from pipeline.chunker    import chunk_text
from pipeline.metadata   import build_metadata
from pipeline.embedder   import embed_chunks
from pipeline.uploader   import upload_batch
from utils.pinecone_client import get_index


def process_one(pdf_path: Path):
    print(f"\nProcessing: {pdf_path.name}")

    raw      = parse_pdf(str(pdf_path))
    clean    = clean_text(raw)
    norm     = normalize_text(clean)
    chunks   = chunk_text(norm, original=clean)
    chunks   = build_metadata(chunks, pdf_path)
    chunks   = embed_chunks(chunks)

    upload_batch(chunks, pdf_path.stem)


def main():
    parser = argparse.ArgumentParser(description="BhaktiSetu ingestion pipeline")
    parser.add_argument(
        "--folder",
        type=str,
        default=str(Path(__file__).parent.parent.parent / "data" / "pdfs"),
        help="Folder containing PDF files (default: data/pdfs/)",
    )
    args = parser.parse_args()

    pdf_dir = Path(args.folder)
    if not pdf_dir.exists():
        print(f"Error: folder '{pdf_dir}' does not exist.")
        print("Create it and drop your PDFs in it, then run again.")
        sys.exit(1)

    pdfs = list(pdf_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in '{pdf_dir}'.")
        sys.exit(1)

    print(f"Found {len(pdfs)} PDFs in '{pdf_dir}'")
    print("Starting ingestion...\n")

    success = 0
    failed  = []

    for pdf in pdfs:
        try:
            process_one(pdf)
            success += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed.append(pdf.name)

    # Final stats from Pinecone
    try:
        index = get_index()
        stats = index.describe_index_stats()
        total_vectors = stats["total_vector_count"]
    except Exception:
        total_vectors = "unknown"

    print("\n" + "=" * 50)
    print(f"Ingestion complete.")
    print(f"  Processed : {success}/{len(pdfs)} PDFs")
    print(f"  Total vectors in Pinecone: {total_vectors}")
    if failed:
        print(f"  Failed files ({len(failed)}):")
        for f in failed:
            print(f"    - {f}")
    print("=" * 50)


if __name__ == "__main__":
    main()