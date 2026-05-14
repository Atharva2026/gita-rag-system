# BhaktiSetu — Phase 1

AI-powered retrieval system for ISKCON lecture transcripts.

---

## Setup

**1. Clone and enter the project**
```bash
git clone <your-repo>
cd bhaktisetu
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file**
```bash
cp .env.example .env
# Open .env and fill in your Pinecone API key
```

**5. Add your PDFs**
```
Drop all lecture PDFs into:  data/pdfs/
```

Recommended filename format: `Lecture_Title__Speaker_Name.pdf`
Example: `Managing_Our_False_Pride__Vraja_Bihari_Das.pdf`

---

## Run ingestion

```bash
python ingestion/pipeline/run.py
```

- First run downloads the embedding model (~2GB) — takes a few minutes
- Each PDF is parsed, cleaned, chunked, embedded, and uploaded to Pinecone
- Safe to re-run — already-uploaded files are automatically skipped
- For a custom folder: `python ingestion/pipeline/run.py --folder /path/to/pdfs`

---

## Test retrieval

After ingestion, verify it's working:

```bash
python test_query.py
```

This runs 3 sample questions and then lets you type your own.
Check that the returned passages are relevant and the source files are correct.

---

## Two-person workflow

Both teammates share one Pinecone index.

1. Person A creates the Pinecone account and shares the `.env` file privately
2. Each person drops their batch of PDFs into `data/pdfs/`
3. Both run `python ingestion/pipeline/run.py` independently
4. Pinecone handles concurrent uploads — no conflicts

---

## Project structure

```
bhaktisetu/
├── ingestion/
│   ├── pipeline/
│   │   ├── run.py          ← entry point (only file you run)
│   │   ├── parser.py       ← PDF → raw text
│   │   ├── cleaner.py      ← remove noise
│   │   ├── normalizer.py   ← fix spelling variants
│   │   ├── chunker.py      ← split into 800-token chunks
│   │   ├── metadata.py     ← speaker, scripture ref, segment type
│   │   ├── embedder.py     ← generate vectors
│   │   └── uploader.py     ← push to Pinecone
│   └── utils/
│       ├── pinecone_client.py
│       └── ocr_fallback.py
├── data/
│   └── pdfs/               ← drop PDFs here
├── test_query.py           ← verify retrieval in IDE
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## What comes after Phase 1

Once retrieval is verified working:

- **Phase 2** — FastAPI backend with `/query` endpoint
- **Phase 3** — Simple React chat UI

No frontend or backend needed until Phase 1 is solid.