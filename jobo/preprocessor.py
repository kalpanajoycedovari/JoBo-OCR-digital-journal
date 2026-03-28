import cv2
import numpy as np


def load_image(path: str) -> np.ndarray:
    """Load an image from disk."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return img


def preprocess(img: np.ndarray) -> np.ndarray:
    """
    Apply a standard preprocessing pipeline to improve OCR accuracy:
      1. Convert to grayscale
      2. Denoise
      3. Adaptive threshold (handles uneven lighting)
      4. Deskew if needed
    """
    gray = _to_grayscale(img)
    denoised = _denoise(gray)
    thresh = _threshold(denoised)
    deskewed = _deskew(thresh)
    return deskewed


# --- Private helpers ---

def _to_grayscale(img: np.ndarray) -> np.ndarray:
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def _denoise(img: np.ndarray) -> np.ndarray:
    # Fast Non-Local Means denoising — good for scanned docs
    return cv2.fastNlMeansDenoising(img, h=10)


def _threshold(img: np.ndarray) -> np.ndarray:
    # Adaptive threshold handles shadows and uneven brightness
    return cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=10
    )


def _deskew(img: np.ndarray) -> np.ndarray:
    """Rotate image to correct slight skew (up to ~10 degrees)."""
    coords = np.column_stack(np.where(img > 0))
    if len(coords) < 5:
        return img
    angle = cv2.minAreaRect(coords)[-1]
    # minAreaRect returns angles in [-90, 0); convert to small rotation
    if angle < -45:
        angle = 90 + angle
    if abs(angle) < 0.5:  # Skip trivial corrections
        return img
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )