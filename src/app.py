"""
app.py — Main application controller for F1 Survey Analytics.

SurveyApp is the orchestrator — it wires together User, Survey,
DataStorage, and Analytics. It handles the menu loop and overall flow.
"""

from auth import User
from survey import Survey
from storage import DataStorage
from analytics import Analytics


class SurveyApp:
    """Main controller that runs the entire F1 Survey program.

    Flow:
    1. Display title
    2. Collect student details (name + student ID) — no authentication
    3. Show menu (Continue / Quit / Restart)
    4. Run survey (adaptive ordering) → display results → confirm → save → show analytics
    """

    def __init__(self, storage_path: str = "data/responses.csv"):
        """Set up the app with all its components.

        Args:
            storage_path: Path to the CSV file for storing responses.
        """
        self._user: User | None = None
        self._survey = Survey()
        self._storage = DataStorage(storage_path)
        self._analytics = Analytics(self._storage)

    def get_student_details(self) -> User:
        """Prompt the student for their name and student ID.

        No authentication — just identification. We record who
        is taking the survey and move on.

        Returns:
            A User object with the student's details.
        """
        print()
        name = input("Enter your name: ").strip()
        student_id = input("Enter your class (student ID): ").strip()
        return User(name, student_id)

    def show_menu(self) -> str:
        """Display the main menu and get the student's choice.

        Returns:
            The validated choice as a string: "1", "2", or "3".
        """
        print(f"\nWelcome {self._user.get_name()} from {self._user.get_student_id()}")
        print("Please choose an option:")
        print("1. Continue")
        print("2. Quit")
        print("3. Restart")

        while True:
            choice = input("Enter your choice (1/2/3): ").strip()
            if choice in ["1", "2", "3"]:
                return choice
            print("Invalid choice. Please enter 1, 2, or 3.")

    def run(self) -> None:
        """Run the full F1 Survey program from start to finish."""
        # ── Title ───────────────────────────────────────────────────
        print(" ==== (F1) FORMULA 1 SURVEY ====")

        # ── Student details (no auth, just identification) ──────────
        self._user = self.get_student_details()

        # ── Menu loop ───────────────────────────────────────────────
        running = True
        while running:
            choice = self.show_menu()

            if choice == "1":
                # ── Continue: Run the survey ────────────────────────
                print(f"\nGood luck with the survey! You chose the option Continue")

                # Collect answers (dict: question_id → letter)
                answers = self._survey.run_survey()

                # Show results for review
                self._survey.display_results(answers)

                # Confirm submission
                if self._survey.confirm_submission():
                    # Save to file
                    self._storage.save_response(self._user, answers)
                    print("Thank you for your time! Your Survey has been submitted.")

                    # Show analytics from all responses
                    self._analytics.generate_summary_report()
                    running = False
                else:
                    print("Ok. Let's return and do the survey again!")
                    # Loop back to menu

            elif choice == "2":
                # ── Quit ────────────────────────────────────────────
                print("See you next time!")
                running = False

            elif choice == "3":
                # ── Restart ─────────────────────────────────────────
                print("Rebooting the survey menu...")
                # Loop back to menu
