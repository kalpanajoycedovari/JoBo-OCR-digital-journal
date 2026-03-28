import os
import pytesseract
from PIL import Image
import numpy as np

# Windows local path
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Linux (Streamlit Cloud)
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def extract_text(img: np.ndarray, lang: str = "eng") -> str:
    """
    Run Tesseract OCR on a preprocessed image.

    Args:
        img:  Preprocessed grayscale/binary image (numpy array).
        lang: Tesseract language code (default English).

    Returns:
        Extracted text as a string.
    """
    pil_img = Image.fromarray(img)
    config = _build_config()
    text = pytesseract.image_to_string(pil_img, lang=lang, config=config)
    return text.strip()


def extract_with_confidence(img: np.ndarray, lang: str = "eng") -> dict:
    """
    Extract text AND per-word confidence scores.

    Returns a dict with:
      - 'text':       full extracted string
      - 'words':      list of dicts {word, confidence, bbox}
      - 'avg_conf':   average confidence (0–100)
    """
    pil_img = Image.fromarray(img)
    config = _build_config()
    data = pytesseract.image_to_data(
        pil_img, lang=lang, config=config,
        output_type=pytesseract.Output.DICT
    )
    words = [
        {
            "word": data["text"][i],
            "confidence": int(data["conf"][i]),
            "bbox": {
                "x": data["left"][i],
                "y": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i],
            }
        }
        for i in range(len(data["text"]))
        if data["text"][i].strip() and int(data["conf"][i]) > 0
    ]
    avg_conf = (
        sum(w["confidence"] for w in words) / len(words) if words else 0
    )
    full_text = " ".join(w["word"] for w in words)
    return {
        "text": full_text,
        "words": words,
        "avg_conf": round(avg_conf, 1)
    }


def _build_config() -> str:
    return "--psm 6 --oem 3"