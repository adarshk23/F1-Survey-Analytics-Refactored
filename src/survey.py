"""
survey.py — Survey engine for F1 Survey Analytics.

Contains the Question class (single question + validation) and
the Survey class (manages questions, collects responses).

FLEXIBLE DESIGN:
- Each question has a stable `id` (e.g. "awareness") used for storage/analytics.
- Each question has a `difficulty` level: "easy", "medium", or "hard".
- Questions are ordered adaptively based on the student's awareness (Q1 answer).
- To add a new question: just append a new dict to SURVEY_DATA below.
  No other code changes needed — storage and analytics adapt automatically.
"""


# ── Question difficulty levels ──────────────────────────────────────
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

# ── All F1 survey questions ────────────────────────────────────────
# To add a new question:
#   1. Add a new dict to this list
#   2. Give it a unique `id` (used as CSV column + analytics key)
#   3. Set `difficulty` to "easy", "medium", or "hard"
#   4. That's it — everything else adapts automatically
#
# The question with id="awareness" MUST come first — it drives
# the adaptive ordering for all remaining questions.

SURVEY_DATA = [
    {
        "id": "awareness",
        "text": "How much knowledge do you hold about F1?",
        "options": ["Zero", "Little", "Some", "A lot"],
        "difficulty": EASY,
        "category": "Awareness",
        "label": "AWARENESS LEVEL",
    },
    {
        "id": "watch_years",
        "text": "How long have you watched F1?",
        "options": ["Between 0-1 Years", "Between 1-3 Years",
                    "Between 3-5 Years", "More than 5 years"],
        "difficulty": EASY,
        "category": "Watch History",
        "label": "WATCH HISTORY (YEARS)",
    },
    {
        "id": "seasons_watched",
        "text": "How many full seasons have you watched in F1?",
        "options": ["None", "1", "2-3", "Greater than 3"],
        "difficulty": EASY,
        "category": "Watch History",
        "label": "SEASONS WATCHED",
    },
    {
        "id": "top_team",
        "text": "What high performing team would you go for?",
        "options": ["McLaren", "Ferrari", "Mercedes", "Red Bull"],
        "difficulty": MEDIUM,
        "category": "Team Preference",
        "label": "FAVOURITE HIGH-PERFORMING TEAM",
    },
    {
        "id": "mid_team",
        "text": "What middle performing team would you go for?",
        "options": ["Williams", "Haas", "Aston Martin", "Alpine"],
        "difficulty": MEDIUM,
        "category": "Team Preference",
        "label": "FAVOURITE MID-PERFORMING TEAM",
    },
    {
        "id": "race_region",
        "text": "Where would you go and watch an F1 race?",
        "options": ["Asia/Southeast Asia", "Europe",
                    "South America", "Middle East"],
        "difficulty": MEDIUM,
        "category": "Viewing Preference",
        "label": "PREFERRED RACE REGION",
    },
    {
        "id": "future_team",
        "text": "Through philosophy, which team do you think will dominate in the future?",
        "options": ["Red Bull", "Mercedes", "Ferrari", "Audi"],
        "difficulty": HARD,
        "category": "Prediction",
        "label": "FUTURE DOMINANT TEAM PREDICTION",
    },
    {
        "id": "legend_driver",
        "text": "Which legendary F1 driver would you pick to race with?",
        "options": ["Ayrton Senna", "Michael Schumacher",
                    "Nigel Mansell", "Damon Hill"],
        "difficulty": HARD,
        "category": "Driver Preference",
        "label": "LEGENDARY DRIVER PICK",
    },
    {
        "id": "dream_team",
        "text": "If you had to drive for an F1 Team, what would it be?",
        "options": ["Mercedes", "Williams", "Ferrari", "McLaren"],
        "difficulty": HARD,
        "category": "Team Preference",
        "label": "DREAM TEAM TO DRIVE FOR",
    },
    {
        "id": "interest",
        "text": "Do you show interest in F1?",
        "options": ["Yes (Rarely)", "Yes (Somewhat)",
                    "Yes (Fully)", "Never"],
        "difficulty": EASY,
        "category": "Interest",
        "label": "INTEREST LEVEL",
    },
]

VALID_ANSWERS = ["A", "B", "C", "D"]

# Difficulty sort orders
_DIFFICULTY_ORDER_EASY_FIRST = {EASY: 0, MEDIUM: 1, HARD: 2}
_DIFFICULTY_ORDER_HARD_FIRST = {HARD: 0, MEDIUM: 1, EASY: 2}


def get_question_ids() -> list[str]:
    """Return the list of all question IDs in definition order.

    Useful for storage and analytics to know what columns exist.
    """
    return [q["id"] for q in SURVEY_DATA]


def get_question_by_id(question_id: str) -> dict | None:
    """Look up a question definition by its ID.

    Args:
        question_id: The unique question ID (e.g. "awareness").

    Returns:
        The question dict, or None if not found.
    """
    for q in SURVEY_DATA:
        if q["id"] == question_id:
            return q
    return None


class Question:
    """A single multiple-choice question with 4 options (A/B/C/D).

    Handles displaying itself and validating the student's input.
    """

    def __init__(self, question_id: str, text: str, options: list[str],
                 difficulty: str = EASY, category: str = "",
                 label: str = "", display_number: int = 0):
        """Create a Question.

        Args:
            question_id: Unique stable ID (e.g. "awareness"). Used for CSV storage.
            text: The question text.
            options: List of 4 option labels.
            difficulty: "easy", "medium", or "hard".
            category: Question category (e.g. "Team Preference").
            label: Short label for analytics reports.
            display_number: Number shown to the student (set during ordering).
        """
        self._id = question_id
        self._text = text
        self._options = options
        self._difficulty = difficulty
        self._category = category
        self._label = label
        self._display_number = display_number

    @property
    def id(self) -> str:
        return self._id

    @property
    def number(self) -> int:
        return self._display_number

    @number.setter
    def number(self, value: int):
        self._display_number = value

    @property
    def text(self) -> str:
        return self._text

    @property
    def options(self) -> list[str]:
        return list(self._options)

    @property
    def difficulty(self) -> str:
        return self._difficulty

    @property
    def category(self) -> str:
        return self._category

    @property
    def label(self) -> str:
        return self._label or self._text

    def display(self) -> None:
        """Print the question and its options to the console."""
        print(f"\n{self._display_number}. {self._text}")
        for i, option in enumerate(self._options):
            letter = VALID_ANSWERS[i]
            print(f"  ({letter}) {option}")

    def get_valid_answer(self) -> str:
        """Prompt the student until they give a valid A/B/C/D answer.

        Returns:
            The validated answer as an uppercase letter (A, B, C, or D).
        """
        while True:
            ans = input("What's your answer? (A/B/C/D): ").strip().upper()
            if ans in VALID_ANSWERS:
                print("Answer Successfully Submitted!")
                return ans
            print("Invalid answer. Please enter A, B, C, or D.")

    def get_option_text(self, letter: str) -> str:
        """Return the option text for a given letter (A/B/C/D).

        Args:
            letter: One of A, B, C, D (uppercase).

        Returns:
            The option label string.
        """
        index = VALID_ANSWERS.index(letter.upper())
        return self._options[index]


class Survey:
    """Manages the F1 survey questions.

    Loads questions from SURVEY_DATA, supports adaptive ordering
    based on student awareness, collects answers, displays results,
    and handles the confirmation prompt.

    ADAPTIVE ORDERING:
    - The awareness question is always asked first.
    - If the student knows little/nothing → easy questions next, hard last.
    - If the student knows some/a lot → hard questions next, easy last.
    - This keeps beginners engaged and challenges experienced fans.
    """

    def __init__(self):
        """Initialise the survey with all questions."""
        self._questions: list[Question] = []
        self._ordered_questions: list[Question] = []
        self._responses: dict[str, str] = {}  # {question_id: answer_letter}
        self.load_questions()

    @property
    def questions(self) -> list[Question]:
        """Return questions in their current display order."""
        return list(self._ordered_questions or self._questions)

    @property
    def responses(self) -> dict[str, str]:
        """Return responses as {question_id: answer_letter}."""
        return dict(self._responses)

    def load_questions(self) -> None:
        """Build Question objects from SURVEY_DATA.

        To add a new question, just add it to SURVEY_DATA above.
        This method picks it up automatically.
        """
        self._questions = []
        for data in SURVEY_DATA:
            self._questions.append(Question(
                question_id=data["id"],
                text=data["text"],
                options=data["options"],
                difficulty=data.get("difficulty", EASY),
                category=data.get("category", ""),
                label=data.get("label", ""),
            ))
        # Default order = definition order
        self._ordered_questions = list(self._questions)
        self._renumber()

    def _renumber(self) -> None:
        """Assign display numbers (1, 2, 3...) to ordered questions."""
        for i, q in enumerate(self._ordered_questions, start=1):
            q.number = i

    def _order_by_awareness(self, awareness_answer: str) -> None:
        """Reorder remaining questions based on awareness level.

        Args:
            awareness_answer: The student's answer to the awareness question.
                A = Zero, B = Little → easy first
                C = Some, D = A lot → hard first
        """
        # Separate awareness question from the rest
        awareness_q = None
        rest = []
        for q in self._questions:
            if q.id == "awareness":
                awareness_q = q
            else:
                rest.append(q)

        # Pick sort order based on awareness
        if awareness_answer in ["A", "B"]:
            # Low awareness → easy first, build up
            order = _DIFFICULTY_ORDER_EASY_FIRST
        else:
            # High awareness → challenging questions first
            order = _DIFFICULTY_ORDER_HARD_FIRST

        # Stable sort: within same difficulty, keep definition order
        rest.sort(key=lambda q: order.get(q.difficulty, 1))

        # Awareness always first
        self._ordered_questions = [awareness_q] + rest if awareness_q else rest
        self._renumber()

    def run_survey(self) -> dict[str, str]:
        """Run the survey with adaptive question ordering.

        1. Ask awareness question first
        2. Reorder remaining questions based on awareness
        3. Ask remaining questions in adapted order
        4. Return all answers keyed by question ID

        Returns:
            Dict mapping question_id → answer_letter.
            Example: {"awareness": "C", "top_team": "B", ...}
        """
        self._responses = {}

        # Step 1: Ask the awareness question first
        awareness_q = None
        for q in self._questions:
            if q.id == "awareness":
                awareness_q = q
                break

        if awareness_q:
            awareness_q.number = 1
            awareness_q.display()
            awareness_ans = awareness_q.get_valid_answer()
            self._responses[awareness_q.id] = awareness_ans

            # Step 2: Reorder based on awareness
            self._order_by_awareness(awareness_ans)

            # Step 3: Ask remaining questions
            for q in self._ordered_questions:
                if q.id == "awareness":
                    continue  # already asked
                q.display()
                answer = q.get_valid_answer()
                self._responses[q.id] = answer
        else:
            # No awareness question — just run in definition order
            self._renumber()
            for q in self._ordered_questions:
                q.display()
                answer = q.get_valid_answer()
                self._responses[q.id] = answer

        return dict(self._responses)

    def display_results(self, responses: dict[str, str]) -> None:
        """Show the student their answers for review.

        Displays in the order questions were asked.

        Args:
            responses: Dict of {question_id: answer_letter}.
        """
        print("\n" + "_" * 30)
        print("FINAL SURVEY RESULTS")
        print("=" * 30)
        for q in self._ordered_questions:
            answer_letter = responses.get(q.id, "?")
            if answer_letter in VALID_ANSWERS:
                answer_text = q.get_option_text(answer_letter)
                print(f"\n{q.number}. {q.text.upper()}")
                print(f"   YOUR ANSWER: ({answer_letter}) {answer_text}")
            else:
                print(f"\n{q.number}. {q.text.upper()}")
                print(f"   YOUR ANSWER: {answer_letter}")
        print()

    def confirm_submission(self) -> bool:
        """Ask the student if they are happy with their answers.

        Returns:
            True if confirmed (Y), False if they want to redo (N).
        """
        while True:
            confirm = input(
                "Are you happy with your answers? (Y/N): "
            ).strip().upper()
            if confirm == "Y":
                return True
            elif confirm == "N":
                return False
            print("Invalid input. Please enter Y or N.")
