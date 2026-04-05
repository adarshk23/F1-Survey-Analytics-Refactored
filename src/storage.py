"""
storage.py — Data persistence for F1 Survey Analytics.

Saves and loads survey responses using CSV files.
Each row = one student's complete survey submission.

CSV columns are built dynamically from question IDs defined in survey.py.
Adding a new question to SURVEY_DATA automatically adds a new CSV column.
Old CSV files with fewer columns still load fine — missing columns get blank values.
"""

import csv
import os
from datetime import datetime

from auth import User
from survey import get_question_ids


def _build_fieldnames() -> list[str]:
    """Build CSV column headers from question IDs.

    Returns:
        List like ["name", "student_id", "timestamp", "awareness", "watch_years", ...]
    """
    return ["name", "student_id", "timestamp"] + get_question_ids()


class DataStorage:
    """Handles reading and writing survey responses to a CSV file.

    The file is created automatically if it doesn't exist.
    New responses are appended — existing data is never overwritten.

    CSV columns adapt to whatever questions are defined in SURVEY_DATA.
    If you add a new question, it automatically becomes a new column.
    Old data files still load — the new column just has blank values
    for previous submissions.
    """

    def __init__(self, file_path: str = "data/responses.csv"):
        """Set up storage with a file path.

        Args:
            file_path: Path to the CSV file. Defaults to data/responses.csv.
        """
        self._file_path = file_path

    @property
    def file_path(self) -> str:
        return self._file_path

    def save_response(self, user: User, responses: dict[str, str]) -> None:
        """Save one student's survey submission to the CSV file.

        Creates the directory and file (with headers) if they don't exist.
        Appends the new row — never overwrites previous data.

        Args:
            user: The User object (name + student_id).
            responses: Dict mapping question_id → answer_letter.
                       Example: {"awareness": "C", "top_team": "B", ...}
        """
        # Create the directory if it doesn't exist
        directory = os.path.dirname(self._file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        fieldnames = _build_fieldnames()

        # Check if we need to write headers (new file)
        file_exists = os.path.exists(self._file_path)

        with open(self._file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header row only for new files
            if not file_exists:
                writer.writeheader()

            # Build the row
            row = {
                "name": user.get_name(),
                "student_id": user.get_student_id(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            # Add each answer by question ID
            for q_id in get_question_ids():
                row[q_id] = responses.get(q_id, "")

            writer.writerow(row)

    def load_all_responses(self) -> list[dict]:
        """Load all saved survey responses from the CSV file.

        Handles old CSV files gracefully — if a column doesn't exist
        in older data, those fields will be empty strings.

        Returns:
            List of dictionaries, one per submission.
            Returns an empty list if the file doesn't exist yet.
        """
        if not os.path.exists(self._file_path):
            return []

        with open(self._file_path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def get_response_count(self) -> int:
        """Return the total number of saved survey responses.

        Returns:
            Integer count of all submissions.
        """
        return len(self.load_all_responses())
