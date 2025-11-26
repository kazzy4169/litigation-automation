from pathlib import Path
from typing import Dict

SUPPORTED_EXTS = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".tiff"}

def normalize_document(doc: Dict, normalized_dir: str) -> Dict:
    src_path = Path(doc["path"])
    ext = doc["ext"]

    normalized_root = Path(normalized_dir)
    normalized_root.mkdir(parents=True, exist_ok=True)

    target_path = normalized_root / src_path.name

    # For now, just copy supported files. Later you can add real conversions.
    if ext in SUPPORTED_EXTS:
        if src_path != target_path:
            target_path.write_bytes(src_path.read_bytes())
    else:
        # Skip unsupported for now; you can log this.
        return {
            "source_path": str(src_path),
            "normalized_path": None,
            "status": "unsupported",
        }

    return {
        "source_path": str(src_path),
        "normalized_path": str(target_path),
        "status": "ok",
    }