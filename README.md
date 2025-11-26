# Litigation Automation – Dedup + OCR Pipeline

This repo contains a Python pipeline to:

- Ingest documents from `data/raw`
- Normalize files to `data/interim`
- Deduplicate using content hashes
- Run OCR / text extraction on canonical docs
- Index text into a SQLite DB
- Emit a JSON report with dedup stats

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

mkdir -p data/raw
# Copy your source files into data/raw

python -m pipeline.cli configs/dedup_ocr.yaml
```

Results will appear in `data/processed/` as:

- `dedup_ocr_report.json`
- `index.sqlite`