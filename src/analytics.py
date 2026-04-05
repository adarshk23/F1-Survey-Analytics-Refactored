"""
analytics.py — Analytics engine for F1 Survey Analytics.

Reads all stored responses and generates:
- Response distributions per question (count + percentage)
- Most popular answer per question
- Awareness & interest level summaries
- Team and driver popularity rankings
- Text-based bar chart visualisations
- A full summary report for CTHS event planning

DYNAMIC: Adapts automatically to whatever questions are defined
in SURVEY_DATA. Add a new question there — analytics picks it up.
"""

from storage import DataStorage
from survey import SURVEY_DATA, VALID_ANSWERS, get_question_ids, get_question_by_id


# Bar chart settings
BAR_FULL = "█"
BAR_EMPTY = "░"
BAR_WIDTH = 20


class Analytics:
    """Generates statistics and visual reports from all survey responses.

    Reads data from DataStorage and produces distributions,
    rankings, and a formatted summary report.

    Fully dynamic — works with any number of questions defined
    in SURVEY_DATA. No hardcoded question numbers.
    """

    def __init__(self, storage: DataStorage):
        """Set up analytics with a DataStorage instance.

        Args:
            storage: The DataStorage to read responses from.
        """
        self._storage = storage

    def response_distribution(self, question_id: str) -> dict:
        """Calculate how many students picked each option for a question.

        Args:
            question_id: The question's unique ID (e.g. "awareness").

        Returns:
            Dict mapping each option letter to its count.
            Example: {"A": 4, "B": 8, "C": 9, "D": 4}
        """
        all_responses = self._storage.load_all_responses()

        # Initialise counts
        counts = {letter: 0 for letter in VALID_ANSWERS}

        for response in all_responses:
            answer = response.get(question_id, "").upper()
            if answer in counts:
                counts[answer] += 1

        return counts

    def most_popular_answer(self, question_id: str) -> str:
        """Find the most picked option for a question.

        Args:
            question_id: The question's unique ID (e.g. "top_team").

        Returns:
            The letter (A/B/C/D) with the highest count.
            If tied, returns the first one alphabetically.
        """
        dist = self.response_distribution(question_id)
        if not any(dist.values()):
            return "N/A"
        return max(dist, key=dist.get)

    def _build_bar(self, count: int, total: int) -> str:
        """Build a text-based bar chart segment.

        Args:
            count: Number of responses for this option.
            total: Total number of responses.

        Returns:
            A string like "████████░░░░░░░░░░░░  40% (10)"
        """
        if total == 0:
            pct = 0
        else:
            pct = round(count / total * 100)

        filled = round(pct / 100 * BAR_WIDTH)
        empty = BAR_WIDTH - filled
        bar = BAR_FULL * filled + BAR_EMPTY * empty
        return f"{bar}  {pct:>3}% ({count})"

    def _print_question_chart(self, question_id: str) -> None:
        """Print a bar chart for one question.

        Args:
            question_id: The question's unique ID.
        """
        q_def = get_question_by_id(question_id)
        if not q_def:
            return

        label = q_def.get("label", question_id.upper())
        options = q_def["options"]
        dist = self.response_distribution(question_id)
        total = sum(dist.values())

        print(f"\n{label}:")
        for i, letter in enumerate(VALID_ANSWERS):
            if i < len(options):
                option_text = options[i]
            else:
                option_text = letter
            count = dist[letter]
            bar = self._build_bar(count, total)
            print(f"  {option_text:<22} {bar}")

    def generate_summary_report(self) -> None:
        """Print the full analytics report to the console.

        Dynamically generates charts for ALL questions defined
        in SURVEY_DATA. Add a new question — it appears here automatically.

        Includes:
        - Total respondent count
        - Bar charts for every question
        - Headline interest summary (if interest question exists)
        - Event recommendation
        """
        all_responses = self._storage.load_all_responses()
        total = len(all_responses)

        # ── Report header ───────────────────────────────────────────
        print("\n" + "═" * 45)
        print("        F1 SURVEY ANALYTICS REPORT")
        print(f"        Total Respondents: {total}")
        print("═" * 45)

        if total == 0:
            print("\nNo responses recorded yet.")
            print("Run the survey to start collecting data!")
            return

        # ── Bar charts for each question (dynamic) ──────────────────
        for q_id in get_question_ids():
            self._print_question_chart(q_id)

        # ── Headline: Interest level summary ────────────────────────
        # Only show if the "interest" question exists
        if get_question_by_id("interest"):
            interest_dist = self.response_distribution("interest")
            # A=Rarely, B=Somewhat, C=Fully → all count as "interested"
            interested = interest_dist["A"] + interest_dist["B"] + interest_dist["C"]
            interest_pct = round(interested / total * 100) if total > 0 else 0

            print("\n" + "─" * 45)
            print(f"HEADLINE: {interest_pct}% of students show some level of F1 interest.")

            if interest_pct >= 70:
                print("RECOMMENDATION: Sufficient interest to proceed with F1 event.")
            elif interest_pct >= 40:
                print("RECOMMENDATION: Moderate interest — consider a smaller F1 activity.")
            else:
                print("RECOMMENDATION: Low interest — F1 event may not be viable.")

            print("─" * 45)

    def display_charts(self) -> None:
        """Alias for generate_summary_report — matches the UML design."""
        self.generate_summary_report()


if __name__ == "__main__":
    print("This module is not the entry point.")
    print("To run the survey:  python3 main.py")
    print("(Run it from the src/ directory)")
