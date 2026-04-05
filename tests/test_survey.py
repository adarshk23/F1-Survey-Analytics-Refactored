"""
test_survey.py — Unit tests for F1 Survey Analytics.

Tests the core classes: User, Question, Survey, DataStorage, Analytics.
Run with:  python3 -m unittest tests/test_survey.py -v
"""

import os
import sys
import csv
import unittest
from unittest.mock import patch
from io import StringIO

# Add src/ to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from auth import User
from survey import (Question, Survey, SURVEY_DATA, VALID_ANSWERS,
                    get_question_ids, get_question_by_id, EASY, MEDIUM, HARD)
from storage import DataStorage, _build_fieldnames
from analytics import Analytics


# ── Helper: build a sample responses dict ───────────────────────────
def _sample_responses(letter: str = "A") -> dict[str, str]:
    """Build a responses dict with the same letter for every question."""
    return {q_id: letter for q_id in get_question_ids()}


class TestUser(unittest.TestCase):
    """Tests for the User data class."""

    def test_create_user(self):
        """User stores name and student_id correctly."""
        user = User("Ahan", "11SEG261")
        self.assertEqual(user.get_name(), "Ahan")
        self.assertEqual(user.get_student_id(), "11SEG261")

    def test_user_repr(self):
        """User has a readable string representation."""
        user = User("Ahan", "11SEG261")
        self.assertIn("Ahan", repr(user))
        self.assertIn("11SEG261", repr(user))


class TestQuestion(unittest.TestCase):
    """Tests for the Question class."""

    def setUp(self):
        self.q = Question(
            question_id="awareness",
            text="How much do you know about F1?",
            options=["Zero", "Little", "Some", "A lot"],
            difficulty=EASY,
            category="Awareness",
            label="AWARENESS LEVEL",
            display_number=1,
        )

    def test_question_properties(self):
        """Question stores id, text, options, difficulty."""
        self.assertEqual(self.q.id, "awareness")
        self.assertEqual(self.q.text, "How much do you know about F1?")
        self.assertEqual(len(self.q.options), 4)
        self.assertEqual(self.q.difficulty, EASY)
        self.assertEqual(self.q.number, 1)

    def test_get_option_text(self):
        """get_option_text maps letter to correct option."""
        self.assertEqual(self.q.get_option_text("A"), "Zero")
        self.assertEqual(self.q.get_option_text("B"), "Little")
        self.assertEqual(self.q.get_option_text("C"), "Some")
        self.assertEqual(self.q.get_option_text("D"), "A lot")

    @patch("builtins.input", return_value="B")
    def test_get_valid_answer_accepts_valid(self, mock_input):
        """Valid answer (B) is accepted on first try."""
        result = self.q.get_valid_answer()
        self.assertEqual(result, "B")

    @patch("builtins.input", side_effect=["b"])
    def test_get_valid_answer_case_insensitive(self, mock_input):
        """Lowercase input is converted to uppercase."""
        result = self.q.get_valid_answer()
        self.assertEqual(result, "B")

    @patch("builtins.input", side_effect=["X", "Z", "A"])
    def test_get_valid_answer_retries_on_invalid(self, mock_input):
        """Invalid inputs are rejected, valid input eventually accepted."""
        result = self.q.get_valid_answer()
        self.assertEqual(result, "A")
        self.assertEqual(mock_input.call_count, 3)

    def test_display_prints_question(self):
        """display() prints the question text and all options."""
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            self.q.display()
            output = mock_out.getvalue()
            self.assertIn("How much do you know about F1?", output)
            self.assertIn("(A) Zero", output)
            self.assertIn("(D) A lot", output)


class TestSurveyData(unittest.TestCase):
    """Tests for the SURVEY_DATA configuration."""

    def test_all_questions_have_required_fields(self):
        """Every question in SURVEY_DATA has id, text, options, difficulty."""
        for q in SURVEY_DATA:
            self.assertIn("id", q, f"Missing 'id' in question: {q.get('text', '?')}")
            self.assertIn("text", q)
            self.assertIn("options", q)
            self.assertIn("difficulty", q)
            self.assertEqual(len(q["options"]), 4, f"Question '{q['id']}' must have 4 options")

    def test_question_ids_are_unique(self):
        """All question IDs are unique."""
        ids = get_question_ids()
        self.assertEqual(len(ids), len(set(ids)), "Duplicate question IDs found")

    def test_awareness_question_exists(self):
        """The awareness question (drives adaptive ordering) must exist."""
        self.assertIsNotNone(get_question_by_id("awareness"))

    def test_get_question_by_id_returns_none_for_unknown(self):
        """Unknown ID returns None."""
        self.assertIsNone(get_question_by_id("nonexistent_question"))

    def test_difficulty_values_are_valid(self):
        """All difficulty values are easy, medium, or hard."""
        valid = {EASY, MEDIUM, HARD}
        for q in SURVEY_DATA:
            self.assertIn(q["difficulty"], valid,
                          f"Invalid difficulty for '{q['id']}': {q['difficulty']}")


class TestSurvey(unittest.TestCase):
    """Tests for the Survey class."""

    def test_loads_all_questions(self):
        """Survey loads all questions from SURVEY_DATA."""
        survey = Survey()
        self.assertEqual(len(survey.questions), len(SURVEY_DATA))

    def test_questions_have_ids(self):
        """All loaded questions have their IDs set."""
        survey = Survey()
        ids = [q.id for q in survey.questions]
        self.assertEqual(ids, get_question_ids())

    @patch("builtins.input", side_effect=["A"] * len(SURVEY_DATA))
    def test_run_survey_returns_dict(self, mock_input):
        """run_survey returns a dict keyed by question ID."""
        survey = Survey()
        answers = survey.run_survey()
        self.assertIsInstance(answers, dict)
        self.assertEqual(len(answers), len(SURVEY_DATA))
        # All answers should be "A"
        for q_id, ans in answers.items():
            self.assertEqual(ans, "A")

    @patch("builtins.input", side_effect=["A"] * len(SURVEY_DATA))
    def test_adaptive_ordering_low_awareness(self, mock_input):
        """Low awareness (A=Zero) → easy questions first after awareness."""
        survey = Survey()
        survey.run_survey()
        # After awareness (easy), next questions should be easy, then medium, then hard
        ordered = survey.questions
        # Skip awareness (index 0), check the rest are sorted by difficulty
        rest = ordered[1:]
        difficulties = [q.difficulty for q in rest]
        # Easy should come before medium, medium before hard
        for i in range(len(difficulties) - 1):
            current_rank = {EASY: 0, MEDIUM: 1, HARD: 2}[difficulties[i]]
            next_rank = {EASY: 0, MEDIUM: 1, HARD: 2}[difficulties[i + 1]]
            self.assertLessEqual(current_rank, next_rank,
                                 f"Easy-first ordering violated at position {i+1}")

    @patch("builtins.input", side_effect=["D"] + ["A"] * (len(SURVEY_DATA) - 1))
    def test_adaptive_ordering_high_awareness(self, mock_input):
        """High awareness (D=A lot) → hard questions first after awareness."""
        survey = Survey()
        survey.run_survey()
        ordered = survey.questions
        rest = ordered[1:]
        difficulties = [q.difficulty for q in rest]
        # Hard should come before medium, medium before easy
        for i in range(len(difficulties) - 1):
            current_rank = {HARD: 0, MEDIUM: 1, EASY: 2}[difficulties[i]]
            next_rank = {HARD: 0, MEDIUM: 1, EASY: 2}[difficulties[i + 1]]
            self.assertLessEqual(current_rank, next_rank,
                                 f"Hard-first ordering violated at position {i+1}")

    @patch("builtins.input", return_value="Y")
    def test_confirm_submission_yes(self, mock_input):
        """Y confirmation returns True."""
        survey = Survey()
        self.assertTrue(survey.confirm_submission())

    @patch("builtins.input", return_value="N")
    def test_confirm_submission_no(self, mock_input):
        """N confirmation returns False."""
        survey = Survey()
        self.assertFalse(survey.confirm_submission())

    def test_display_results_output(self):
        """display_results prints question text and answers."""
        survey = Survey()
        answers = _sample_responses("C")
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            survey.display_results(answers)
            output = mock_out.getvalue()
            self.assertIn("FINAL SURVEY RESULTS", output)
            self.assertIn("YOUR ANSWER:", output)


class TestDataStorage(unittest.TestCase):
    """Tests for the DataStorage class (CSV persistence)."""

    def setUp(self):
        """Use a temp file for each test."""
        self.test_file = "tmp_rovodev_test_responses.csv"
        self.storage = DataStorage(self.test_file)

    def tearDown(self):
        """Clean up the temp file after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_creates_file(self):
        """Saving a response creates the CSV file."""
        user = User("Ahan", "11SEG261")
        self.storage.save_response(user, _sample_responses("A"))
        self.assertTrue(os.path.exists(self.test_file))

    def test_save_and_load_roundtrip(self):
        """Saved response can be loaded back correctly."""
        user = User("Ahan", "11SEG261")
        answers = _sample_responses("C")
        answers["awareness"] = "D"  # override one
        self.storage.save_response(user, answers)

        loaded = self.storage.load_all_responses()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["name"], "Ahan")
        self.assertEqual(loaded[0]["student_id"], "11SEG261")
        self.assertEqual(loaded[0]["awareness"], "D")
        self.assertEqual(loaded[0]["interest"], "C")

    def test_multiple_saves_append(self):
        """Multiple saves append rows, not overwrite."""
        user1 = User("Ahan", "11SEG261")
        user2 = User("Max", "11SEG261")

        self.storage.save_response(user1, _sample_responses("A"))
        self.storage.save_response(user2, _sample_responses("B"))

        loaded = self.storage.load_all_responses()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["name"], "Ahan")
        self.assertEqual(loaded[1]["name"], "Max")

    def test_load_empty_when_no_file(self):
        """Loading from a non-existent file returns empty list."""
        storage = DataStorage("nonexistent_file.csv")
        self.assertEqual(storage.load_all_responses(), [])

    def test_get_response_count(self):
        """get_response_count returns correct number."""
        user = User("Test", "11SEG261")
        self.assertEqual(self.storage.get_response_count(), 0)
        self.storage.save_response(user, _sample_responses("A"))
        self.assertEqual(self.storage.get_response_count(), 1)

    def test_csv_has_question_id_headers(self):
        """CSV headers include question IDs, not q1/q2/q3."""
        user = User("Ahan", "11SEG261")
        self.storage.save_response(user, _sample_responses("A"))

        with open(self.test_file, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            # Should contain question IDs like "awareness", "top_team" etc
            self.assertIn("awareness", headers)
            self.assertIn("interest", headers)
            self.assertIn("top_team", headers)
            # Should NOT contain old positional names
            self.assertNotIn("q1", headers)

    def test_fieldnames_match_question_ids(self):
        """_build_fieldnames includes all current question IDs."""
        fieldnames = _build_fieldnames()
        self.assertIn("name", fieldnames)
        self.assertIn("student_id", fieldnames)
        self.assertIn("timestamp", fieldnames)
        for q_id in get_question_ids():
            self.assertIn(q_id, fieldnames)


class TestAnalytics(unittest.TestCase):
    """Tests for the Analytics class."""

    def setUp(self):
        """Create a storage with test data."""
        self.test_file = "tmp_rovodev_test_analytics.csv"
        self.storage = DataStorage(self.test_file)
        self.analytics = Analytics(self.storage)

        # Add 4 test responses with varied answers
        test_users = [
            ("Alice", {"awareness": "A", "watch_years": "A", "seasons_watched": "A",
                       "top_team": "B", "mid_team": "A", "race_region": "B",
                       "future_team": "A", "legend_driver": "A", "dream_team": "C",
                       "interest": "C"}),
            ("Bob",   {"awareness": "B", "watch_years": "B", "seasons_watched": "B",
                       "top_team": "B", "mid_team": "C", "race_region": "A",
                       "future_team": "C", "legend_driver": "B", "dream_team": "A",
                       "interest": "C"}),
            ("Carol", {"awareness": "C", "watch_years": "C", "seasons_watched": "C",
                       "top_team": "A", "mid_team": "A", "race_region": "B",
                       "future_team": "C", "legend_driver": "A", "dream_team": "C",
                       "interest": "B"}),
            ("Dave",  {"awareness": "D", "watch_years": "D", "seasons_watched": "D",
                       "top_team": "B", "mid_team": "D", "race_region": "C",
                       "future_team": "B", "legend_driver": "D", "dream_team": "D",
                       "interest": "A"}),
        ]
        for name, answers in test_users:
            user = User(name, "11SEG261")
            self.storage.save_response(user, answers)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_response_distribution(self):
        """Distribution counts each option correctly for awareness."""
        dist = self.analytics.response_distribution("awareness")
        # Alice=A, Bob=B, Carol=C, Dave=D → 1 each
        self.assertEqual(dist, {"A": 1, "B": 1, "C": 1, "D": 1})

    def test_response_distribution_top_team(self):
        """Distribution counts correctly when answers cluster."""
        dist = self.analytics.response_distribution("top_team")
        # Alice=B, Bob=B, Carol=A, Dave=B → A:1, B:3
        self.assertEqual(dist["A"], 1)
        self.assertEqual(dist["B"], 3)
        self.assertEqual(dist["C"], 0)
        self.assertEqual(dist["D"], 0)

    def test_most_popular_answer(self):
        """Most popular answer for top_team is B (Ferrari — 3 picks)."""
        result = self.analytics.most_popular_answer("top_team")
        self.assertEqual(result, "B")

    def test_most_popular_answer_tie(self):
        """When tied, most_popular_answer returns a valid letter."""
        result = self.analytics.most_popular_answer("awareness")
        self.assertIn(result, VALID_ANSWERS)

    def test_most_popular_no_data(self):
        """No data returns N/A."""
        empty_storage = DataStorage("tmp_rovodev_empty.csv")
        empty_analytics = Analytics(empty_storage)
        result = empty_analytics.most_popular_answer("awareness")
        self.assertEqual(result, "N/A")

    def test_generate_summary_report_runs(self):
        """Summary report prints without errors."""
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            self.analytics.generate_summary_report()
            output = mock_out.getvalue()
            self.assertIn("F1 SURVEY ANALYTICS REPORT", output)
            self.assertIn("Total Respondents: 4", output)
            self.assertIn("AWARENESS LEVEL", output)
            self.assertIn("INTEREST LEVEL", output)

    def test_generate_summary_report_empty(self):
        """Summary report handles zero responses gracefully."""
        empty_storage = DataStorage("tmp_rovodev_empty.csv")
        empty_analytics = Analytics(empty_storage)
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            empty_analytics.generate_summary_report()
            output = mock_out.getvalue()
            self.assertIn("No responses recorded yet", output)


if __name__ == "__main__":
    unittest.main()
