"""
auth.py — User identification for F1 Survey Analytics.

This module handles collecting student details (name and student ID).
No authentication is performed — this is identification only.
"""


class User:
    """Holds student details — name and student ID (class code).

    This is a simple data object. No passwords, no login checks.
    We just record who is taking the survey.
    """

    def __init__(self, name: str, student_id: str):
        """Create a User with their name and student ID.

        Args:
            name: The student's name (e.g. "Ahan Kesharwani").
            student_id: The student's class code (e.g. "11SEG261").
        """
        self._name = name
        self._student_id = student_id

    def get_name(self) -> str:
        """Return the student's name."""
        return self._name

    def get_student_id(self) -> str:
        """Return the student's class code / student ID."""
        return self._student_id

    def __repr__(self) -> str:
        return f"User(name='{self._name}', student_id='{self._student_id}')"
