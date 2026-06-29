import re
from collections import Counter


def repetition_signal(text):
    """
    Returns a score between 0 and 1.

    Higher score = more repetitive
    (slightly more AI-like)
    """

    words = re.findall(r"\b\w+\b", text.lower())

    if len(words) < 5:
        return 0.5

    counts = Counter(words)

    repeated = sum(
        count - 1
        for count in counts.values()
        if count > 1
    )

    repetition_ratio = repeated / len(words)

    return round(min(repetition_ratio * 2, 1), 3)