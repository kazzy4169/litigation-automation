import sys
from typing import List, Dict

from tqdm import tqdm

from .config import load_config
from .ingest import iter_documents
from .normalize import normalize_document
from .deduplicate import exact_deduplicate
from .ocr import ocr_document
from .index import index_documents_sqlite
from .report import generate_report

def run_pipeline(config_path: str):
    cfg = load_config(config_path)

    input_dir = cfg["input_dir"]
    normalized_dir = cfg["normalized_dir"]
    output_dir = cfg["output_dir"]

    ocr_cfg = cfg.get("ocr", {})
    dedup_cfg = cfg.get("dedup", {})
    index_cfg = cfg.get("index", {})
    report_cfg = cfg.get("report", {})

    docs: List[Dict] = []

    for doc in tqdm(iter_documents(input_dir), desc="Ingesting documents"):
        docs.append(doc)

    normalized_docs: List[Dict] = []
    for doc in tqdm(docs, desc="Normalizing documents"):
        norm = normalize_document(doc, normalized_dir)
        normalized_docs.append(norm)

    canonical_docs, duplicate_docs = exact_deduplicate(
        normalized_docs,
        hash_algo=dedup_cfg.get("exact", {}).get("hash_algorithm", "sha256"),
    )

    ocr_enabled = ocr_cfg.get("enabled", True)
    if ocr_enabled:
        for d in tqdm(canonical_docs, desc="Running OCR"):
            ocr_document(
                d,
                ocr_lang=ocr_cfg.get("language", "eng"),
            )

    if index_cfg.get("enabled", True):
        db_path = index_cfg.get("sqlite_path", "data/processed/index.sqlite")
        index_documents_sqlite(db_path, canonical_docs)

    report_path = report_cfg.get(
        "output_path",
        "data/processed/dedup_ocr_report.json",
    )
    generate_report(
        all_docs=normalized_docs,
        canonical_docs=canonical_docs,
        duplicate_docs=duplicate_docs,
        output_path=report_path,
    )

def main():
    if len(sys.argv) < 2:
        config_path = "configs/dedup_ocr.yaml"
    else:
        config_path = sys.argv[1]
    run_pipeline(config_path)

if __name__ == "__main__":
    main()