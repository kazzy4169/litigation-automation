from typing import List, Dict
import json
from pathlib import Path

def generate_report(
    all_docs: List[Dict],
    canonical_docs: List[Dict],
    duplicate_docs: List[Dict],
    output_path: str,
):
    report = {
        "total_files_seen": len(all_docs),
        "canonical_count": len(canonical_docs),
        "duplicate_count": len(duplicate_docs),
        "dedup_ratio": (
            1.0 - (len(canonical_docs) / len(all_docs))
            if all_docs
            else 0.0
        ),
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)