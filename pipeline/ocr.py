from typing import Dict
from pathlib import Path

from PIL import Image
import pytesseract

def is_image(ext: str) -> bool:
    return ext.lower() in [".png", ".jpg", ".jpeg", ".tiff"]

def run_ocr_on_image(path: str, lang: str = "eng") -> str:
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def ocr_document(doc: Dict, ocr_lang: str = "eng") -> Dict:
    norm_path = doc.get("normalized_path")
    if not norm_path:
        doc["text"] = ""
        doc["ocr_status"] = "no_normalized_path"
        return doc

    ext = Path(norm_path).suffix.lower()

    # Simple starter: OCR images, leave PDFs/docx for later.
    if is_image(ext):
        text = run_ocr_on_image(norm_path, lang=ocr_lang)
        doc["text"] = text
        doc["ocr_status"] = "ocr_done"
    else:
        # TODO: plug in pdfminer / docx text extraction
        doc["text"] = ""
        doc["ocr_status"] = "skipped_non_image"

    return doc