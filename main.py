"""
JoBo – OCR Digital Journal
CLI entry point — Phase 2 (storage + search).

Usage:
    python main.py --image uploads/photo.jpg
    python main.py --image uploads/photo.jpg --verbose
    python main.py --list
    python main.py --search "hello"
    python main.py --delete 1
"""

import argparse

from jobo.preprocessor import load_image, preprocess
from jobo.ocr_engine import extract_text, extract_with_confidence
from jobo.database import init_db, save_entry, get_all_entries, delete_entry
from jobo.models import JournalEntry
from jobo.search import search_entries


def cmd_process(image_path: str, verbose: bool) -> None:
    print(f"\n[JoBo] Processing: {image_path}")

    img = load_image(image_path)
    print("  ✓ Image loaded")

    processed = preprocess(img)
    print("  ✓ Preprocessing done")

    if verbose:
        result = extract_with_confidence(processed)
        text = result["text"]
        confidence = result["avg_conf"]
        print(f"  ✓ OCR complete — avg confidence: {confidence}%")
    else:
        text = extract_text(processed)
        confidence = 0.0
        print("  ✓ OCR complete")

    if not text:
        print("  ✗ No text detected. Entry not saved.")
        return

    entry = JournalEntry(
        image_path=image_path,
        extracted_text=text,
        confidence=confidence
    )
    saved = save_entry(entry)
    print(f"  ✓ Entry saved with ID: {saved.id}")

    print("\n--- Extracted Text ---")
    print(text)
    print("----------------------")


def cmd_list() -> None:
    entries = get_all_entries()
    if not entries:
        print("\nNo entries found.")
        return
    print(f"\n[JoBo] {len(entries)} journal entry/entries:\n")
    for e in entries:
        print(e)


def cmd_search(keyword: str) -> None:
    results = search_entries(keyword)
    if not results:
        print(f"\nNo entries found for: '{keyword}'")
        return
    print(f"\n[JoBo] {len(results)} result(s) for '{keyword}':\n")
    for e in results:
        print(e)


def cmd_delete(entry_id: int) -> None:
    if delete_entry(entry_id):
        print(f"\n  ✓ Entry {entry_id} deleted.")
    else:
        print(f"\n  ✗ No entry found with ID {entry_id}.")


if __name__ == "__main__":
    init_db()

    parser = argparse.ArgumentParser(description="JoBo OCR Journal")
    parser.add_argument("--image",   help="Path to image file to process")
    parser.add_argument("--verbose", action="store_true", help="Show confidence scores")
    parser.add_argument("--list",    action="store_true", help="List all journal entries")
    parser.add_argument("--search",  help="Search entries by keyword")
    parser.add_argument("--delete",  type=int, help="Delete an entry by ID")
    args = parser.parse_args()

    if args.image:
        cmd_process(args.image, args.verbose)
    elif args.list:
        cmd_list()
    elif args.search:
        cmd_search(args.search)
    elif args.delete:
        cmd_delete(args.delete)
    else:
        parser.print_help()