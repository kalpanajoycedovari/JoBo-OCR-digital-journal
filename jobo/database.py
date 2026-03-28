import sqlite3
import os
from jobo.models import JournalEntry

DB_PATH = "jobo_journal.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the journal_entries table if it doesn't exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path  TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            confidence  REAL NOT NULL,
            created_at  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"  ✓ Database ready at {DB_PATH}")


def save_entry(entry: JournalEntry) -> JournalEntry:
    """Insert a new journal entry and return it with its assigned id."""
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO journal_entries (image_path, extracted_text, confidence, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (entry.image_path, entry.extracted_text, entry.confidence, entry.created_at)
    )
    conn.commit()
    entry.id = cursor.lastrowid
    conn.close()
    return entry


def get_all_entries() -> list[JournalEntry]:
    """Return all journal entries, newest first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM journal_entries ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [_row_to_entry(r) for r in rows]


def get_entry_by_id(entry_id: int) -> JournalEntry | None:
    """Return a single entry by its id."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM journal_entries WHERE id = ?", (entry_id,)
    ).fetchone()
    conn.close()
    return _row_to_entry(row) if row else None


def delete_entry(entry_id: int) -> bool:
    """Delete an entry by id. Returns True if deleted."""
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM journal_entries WHERE id = ?", (entry_id,)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def _row_to_entry(row: sqlite3.Row) -> JournalEntry:
    return JournalEntry(
        id=row["id"],
        image_path=row["image_path"],
        extracted_text=row["extracted_text"],
        confidence=row["confidence"],
        created_at=row["created_at"]
    )