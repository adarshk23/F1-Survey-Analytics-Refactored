"""
main.py — Entry point for F1 Survey Analytics.

Run this file to start the survey program:
    python main.py
"""

from app import SurveyApp


def main():
    """Create and run the F1 Survey application."""
    app = SurveyApp()
    app.run()


if __name__ == "__main__":
    main()
