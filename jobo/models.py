from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class JournalEntry:
    """Represents a single OCR journal entry."""
    image_path: str
    extracted_text: str
    confidence: float
    id: int = None
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def preview(self, chars: int = 80) -> str:
        """Return a short preview of the extracted text."""
        text = self.extracted_text.strip()
        return text[:chars] + "..." if len(text) > chars else text

    def __str__(self):
        return (
            f"[{self.id}] {self.created_at}\n"
            f"  Image : {self.image_path}\n"
            f"  Conf  : {self.confidence}%\n"
            f"  Text  : {self.preview()}\n"
        )