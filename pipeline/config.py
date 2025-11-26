import yaml
from pathlib import Path

def load_config(config_path: str = "configs/dedup_ocr.yaml") -> dict:
    config_file = Path(config_path)
    with config_file.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg