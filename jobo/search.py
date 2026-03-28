import sqlite3
from jobo.database import get_connection
from jobo.models import JournalEntry


def search_entries(keyword: str) -> list[JournalEntry]:
    """
    Search journal entries whose extracted text contains the keyword.
    Case-insensitive.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM journal_entries
        WHERE LOWER(extracted_text) LIKE LOWER(?)
        ORDER BY created_at DESC
        """,
        (f"%{keyword}%",)
    ).fetchall()
    conn.close()
    return [_row_to_entry(r) for r in rows]


def search_by_date(date_str: str) -> list[JournalEntry]:
    """
    Search entries by date (e.g. '2024-03' matches all entries in March 2024).
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM journal_entries
        WHERE created_at LIKE ?
        ORDER BY created_at DESC
        """,
        (f"{date_str}%",)
    ).fetchall()
    conn.close()
    return [_row_to_entry(r) for r in rows]


def _row_to_entry(row: sqlite3.Row) -> JournalEntry:
    return JournalEntry(
        id=row["id"],
        image_path=row["image_path"],
        extracted_text=row["extracted_text"],
        confidence=row["confidence"],
        created_at=row["created_at"]
    )