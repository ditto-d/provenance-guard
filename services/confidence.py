def combine_scores(llm_score, stylometric_score, repetition_score):
    """
    Weighted ensemble.

    LLM carries most of the decision because it captures semantics.
    Stylometric features provide supporting evidence.
    Repetition is a weak heuristic.
    """

    confidence = (
        llm_score * 0.70
        + stylometric_score * 0.20
        + repetition_score * 0.10
    )

    return round(confidence, 3)


def determine_classification(confidence):
    """
    Maps confidence to a final attribution.
    """

    if confidence >= 0.75:
        return "likely_ai"

    elif confidence <= 0.35:
        return "likely_human"

    return "uncertain"