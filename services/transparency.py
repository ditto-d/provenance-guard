def get_transparency_label(classification, confidence):

    if classification == "likely_ai":
        return (
            "Likely AI-generated. "
            "Our analysis found strong indicators that this content was generated "
            "using artificial intelligence. This assessment is made with high confidence, "
            "but creators may appeal if they believe this decision is incorrect."
        )

    if classification == "likely_human":
        return (
            "Likely human-written. "
            "Our analysis found strong indicators of human authorship. "
            "While no automated system is perfect, this content appears to have "
            "been written by a person."
        )

    return (
        "Unable to determine confidently. "
        "The available evidence is mixed, so we cannot confidently classify "
        "this content as either AI-generated or human-written. "
        "No definitive attribution has been made."
    )