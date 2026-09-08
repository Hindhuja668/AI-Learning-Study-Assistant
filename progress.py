import json
import os


PROGRESS_FILE = "progress.json"


def save_progress(score, total_questions):

    progress = []

    if os.path.exists(PROGRESS_FILE):

        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)

    progress.append(
        {
            "score": score,
            "total": total_questions
        }
    )

    with open(PROGRESS_FILE, "w") as f:
        json.dump(
            progress,
            f,
            indent=4
        )


def get_progress():

    if not os.path.exists(PROGRESS_FILE):
        return []

    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)