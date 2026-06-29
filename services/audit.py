import json
import os
from datetime import datetime, timezone
from config import AUDIT_LOG_PATH


def _initialize_log():
    """
    Creates the audit log file if it does not already exist.
    """
    directory = os.path.dirname(AUDIT_LOG_PATH)

    if directory:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, "w") as f:
            json.dump([], f, indent=4)


def get_audit_log():
    """
    Returns every audit log entry.
    """
    _initialize_log()

    with open(AUDIT_LOG_PATH, "r") as f:
        return json.load(f)


def save_audit_log(entries):
    """
    Writes all entries back to disk.
    """
    with open(AUDIT_LOG_PATH, "w") as f:
        json.dump(entries, f, indent=4)


def log_submission(
    content_id,
    creator_id,
    classification,
    confidence,
    signals,
    transparency_label,
    status
):
    """
    Records a content submission.
    """

    entries = get_audit_log()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "content_id": content_id,

        "creator_id": creator_id,

        "classification": classification,

        "confidence": confidence,

        "signals": signals,

        "transparency_label": transparency_label,

        "status": status,

        "appeal": None
    }

    entries.append(entry)

    save_audit_log(entries)


def find_submission(content_id):
    """
    Finds one submission by ID.
    """

    entries = get_audit_log()

    for entry in entries:
        if entry["content_id"] == content_id:
            return entry

    return None


def update_submission(updated_entry):
    """
    Replaces an existing submission.
    """

    entries = get_audit_log()

    for i, entry in enumerate(entries):
        if entry["content_id"] == updated_entry["content_id"]:
            entries[i] = updated_entry
            break

    save_audit_log(entries)