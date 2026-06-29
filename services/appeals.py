from services.audit import (
    find_submission,
    update_submission,
)


def submit_appeal(content_id, creator_reasoning):
    """
    Marks an existing submission as under review
    and records the creator's appeal.
    """

    submission = find_submission(content_id)

    if submission is None:
        return None

    submission["status"] = "under_review"

    submission["appeal"] = {
        "creator_reasoning": creator_reasoning,
        "review_status": "pending"
    }

    update_submission(submission)

    return submission