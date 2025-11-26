from pathlib import Path
from typing import Dict, Iterator

def iter_documents(input_dir: str) -> Iterator[Dict]:
    root = Path(input_dir)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        yield {
            "path": str(path),
            "name": path.name,
            "ext": path.suffix.lower(),
        }