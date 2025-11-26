import hashlib
from typing import Dict, List, Tuple
from pathlib import Path

def file_hash(path: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def exact_deduplicate(docs: List[Dict], hash_algo: str = "sha256") -> Tuple[List[Dict], List[Dict]]:
    hash_to_docs = {}
    for doc in docs:
        norm_path = doc.get("normalized_path")
        if not norm_path:
            continue
        h = file_hash(norm_path, hash_algo)
        doc["content_hash"] = h
        hash_to_docs.setdefault(h, []).append(doc)

    canonical = []
    duplicates = []
    for h, group in hash_to_docs.items():
        if len(group) == 1:
            canonical.append(group[0])
        else:
            group_sorted = sorted(group, key=lambda d: d["source_path"])
            canonical_doc = group_sorted[0]
            canonical_doc["dupe_group_id"] = h
            canonical.append(canonical_doc)
            for d in group_sorted[1:]:
                d["dupe_group_id"] = h
                duplicates.append(d)

    return canonical, duplicates