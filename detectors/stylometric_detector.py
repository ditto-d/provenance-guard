import re
import statistics


def stylometric_signal(text):
    """
    Returns a score between 0 and 1.
    Higher = more AI-like.
    """

    # Split sentences
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0.5

    words = re.findall(r"\b\w+\b", text.lower())

    if not words:
        return 0.5

    # ---------- Feature 1 ----------
    # Sentence length variance

    sentence_lengths = [
        len(re.findall(r"\b\w+\b", s))
        for s in sentences
    ]

    variance = (
        statistics.pvariance(sentence_lengths)
        if len(sentence_lengths) > 1
        else 0
    )

    variance_score = max(
        0,
        min(1, 1 - variance / 40)
    )

    # ---------- Feature 2 ----------
    # Vocabulary diversity

    unique_words = len(set(words))
    ttr = unique_words / len(words)

    ttr_score = max(
        0,
        min(1, 1 - ttr)
    )

    # ---------- Feature 3 ----------
    # Punctuation density

    punctuation = len(re.findall(r"[,:;!?]", text))

    punctuation_density = punctuation / max(len(words), 1)

    punctuation_score = max(
        0,
        min(1, punctuation_density * 4)
    )

    score = (
        variance_score +
        ttr_score +
        punctuation_score
    ) / 3

    return round(score, 3)