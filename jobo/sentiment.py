from textblob import TextBlob


def analyse_sentiment(text: str) -> dict:
    """
    Analyse the sentiment of a given text.

    Returns a dict with:
      - polarity:     float from -1.0 (negative) to 1.0 (positive)
      - subjectivity: float from 0.0 (objective) to 1.0 (subjective)
      - label:        "Positive", "Negative", or "Neutral"
      - emoji:        visual indicator of mood
    """
    if not text or not text.strip():
        return {
            "polarity": 0.0,
            "subjectivity": 0.0,
            "label": "Neutral",
            "emoji": "😐"
        }

    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    if polarity > 0.1:
        label = "Positive"
        emoji = "😊"
    elif polarity < -0.1:
        label = "Negative"
        emoji = "😔"
    else:
        label = "Neutral"
        emoji = "😐"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "label": label,
        "emoji": emoji
    }


def get_sentiment_summary(entries: list) -> dict:
    """
    Given a list of JournalEntry objects, return an overall
    sentiment breakdown across all entries.
    """
    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    total_polarity = 0.0

    for entry in entries:
        result = analyse_sentiment(entry.extracted_text)
        counts[result["label"]] += 1
        total_polarity += result["polarity"]

    total = len(entries)
    avg_polarity = round(total_polarity / total, 3) if total > 0 else 0.0

    return {
        "counts": counts,
        "avg_polarity": avg_polarity,
        "total": total
    }