# F1 Survey Analytics — Design Document

## Project Overview

**Project Name:** F1 Survey Analytics
**Author:** Ahan Kesharwani (Class 11SEG261)
**Phase:** Design & Architecture

## What Are We Building?

A Python program that captures student responses about Formula 1 (F1) motorsport — their awareness, preferences, likes, and dislikes — and produces **analytics** from the collected data.

## Goals

| # | Goal | Description |
|---|------|-------------|
| 1 | **Capture Responses** | Run a 10-question multiple-choice survey on F1 topics |
| 2 | **Authenticate Users** | Gate access using a class code so only valid students participate |
| 3 | **Validate Input** | Ensure all responses are valid (A/B/C/D only) |
| 4 | **Store Results** | Persist survey responses to file (CSV/JSON) so data isn't lost |
| 5 | **Generate Analytics** | Analyse response patterns — popularity of teams, knowledge levels, viewing habits |
| 6 | **Display Results** | Show individual results back to the user + aggregated analytics |

## Survey Topics (10 Questions)

1. F1 knowledge level
2. Years watching F1
3. Full seasons watched
4. Preferred high-performing team
5. Preferred mid-performing team
6. Preferred race location
7. Future dominant team prediction
8. Legendary driver pick
9. Dream team to drive for
10. Overall F1 interest level

---

## UML Class Diagram

This diagram shows the **classes and their relationships** for the refactored program. The original code is a flat script — this design breaks it into proper objects.

```mermaid
classDiagram
    direction TB

    class SurveyApp {
        -authenticator: Authenticator
        -survey: Survey
        -storage: DataStorage
        -analytics: Analytics
        +run() void
        +show_menu() str
    }

    class Authenticator {
        -valid_class_code: str
        +get_user_details() User
        +validate_access(class_code: str) bool
    }

    class User {
        -name: str
        -class_code: str
        +get_name() str
        +get_class_code() str
    }

    class Survey {
        -questions: list~Question~
        -responses: list~str~
        +load_questions() void
        +run_survey() list~str~
        +display_results(responses: list) void
        +confirm_submission() bool
    }

    class Question {
        -number: int
        -text: str
        -options: list~str~
        +display() void
        +get_valid_answer() str
    }

    class DataStorage {
        -file_path: str
        +save_response(user: User, responses: list) void
        +load_all_responses() list~dict~
        +export_csv() void
    }

    class Analytics {
        -storage: DataStorage
        +most_popular_answer(question_num: int) str
        +response_distribution(question_num: int) dict
        +generate_summary_report() void
        +display_charts() void
    }

    SurveyApp --> Authenticator : uses
    SurveyApp --> Survey : uses
    SurveyApp --> DataStorage : uses
    SurveyApp --> Analytics : uses
    Authenticator --> User : creates
    Survey --> Question : contains 1..*
    Analytics --> DataStorage : reads from
```

### Class Responsibilities

| Class | Responsibility |
|-------|---------------|
| **SurveyApp** | Main controller — orchestrates the entire flow (menu, auth, survey, analytics) |
| **Authenticator** | Handles user identification and class code validation |
| **User** | Data object holding student name and class code |
| **Survey** | Manages the 10 questions, collects responses, displays results |
| **Question** | Single question with its text and options; handles input validation |
| **DataStorage** | Saves/loads survey responses to/from file (CSV or JSON) |
| **Analytics** | Reads stored data and generates statistics (popular answers, distributions) |

---

## Sequence Diagram

This diagram shows **how the program flows** from start to finish — the order of interactions between the user and the system components.

### Main Flow — Happy Path (User completes survey)

```mermaid
sequenceDiagram
    actor Student
    participant App as SurveyApp
    participant Auth as Authenticator
    participant Survey as Survey
    participant Q as Question
    participant Store as DataStorage
    participant Stats as Analytics

    Student->>App: Start program
    App->>App: Display title "F1 FORMULA 1 SURVEY"

    rect rgb(240, 248, 255)
        Note over Student, Auth: Authentication Phase
        App->>Auth: get_user_details()
        Auth->>Student: Prompt "Enter your name"
        Student-->>Auth: name
        Auth->>Student: Prompt "Enter your class"
        Student-->>Auth: class_code
        Auth->>Auth: validate_access(class_code)
        alt Invalid class code
            Auth-->>App: Access Denied
            App-->>Student: "Sorry. Access Denied."
            Note over App: Program exits
        else Valid class code
            Auth-->>App: User object created
        end
    end

    rect rgb(245, 255, 245)
        Note over Student, Survey: Menu Phase
        loop Menu Loop (while running)
            App->>Student: Show menu (Continue / Quit / Restart)
            Student-->>App: choice

            alt Choice = 1 (Continue)
                App->>Survey: run_survey()

                rect rgb(255, 255, 240)
                    Note over Student, Q: Survey Phase (10 Questions)
                    loop For each Question (1-10)
                        Survey->>Q: display()
                        Q->>Student: Show question + options (A/B/C/D)
                        Student-->>Q: answer
                        Q->>Q: Validate answer
                        alt Invalid answer
                            Q->>Student: "Invalid. Enter A, B, C, or D"
                            Student-->>Q: corrected answer
                        end
                        Q-->>Survey: valid answer
                        Survey->>Survey: answers.append(answer)
                    end
                end

                Survey->>Survey: display_results(answers)
                Survey->>Student: Show all Q&A pairs

                rect rgb(255, 240, 245)
                    Note over Student, Store: Confirmation & Storage Phase
                    Survey->>Student: "Happy with answers? (Y/N)"
                    Student-->>Survey: confirmation

                    alt Confirm = Y (Happy)
                        Survey-->>App: answers confirmed
                        App->>Store: save_response(user, answers)
                        Store->>Store: Write to file
                        App->>Stats: generate_summary_report()
                        Stats->>Store: load_all_responses()
                        Stats->>Stats: Calculate distributions
                        Stats->>Student: Display analytics
                        App-->>Student: "Thank you! Survey submitted."
                        Note over App: running = False
                    else Confirm = N (Not happy)
                        Survey-->>App: restart survey
                        Note over App: Loop back to menu
                    end
                end

            else Choice = 2 (Quit)
                App-->>Student: "See you next time!"
                Note over App: running = False

            else Choice = 3 (Restart)
                App-->>Student: "Rebooting survey menu..."
                Note over App: Loop back to menu
            end
        end
    end
```

### Sequence Diagram — What It Shows

| Phase | What Happens |
|-------|-------------|
| **Authentication** | Student enters name + class code → validated against 11SEG261 |
| **Menu** | Student picks Continue, Quit, or Restart |
| **Survey** | 10 questions displayed one-by-one, each answer validated (A/B/C/D only) |
| **Results** | All answers displayed back to the student for review |
| **Confirmation** | Student confirms (Y) to submit or (N) to redo |
| **Storage** | Confirmed answers saved to file (NEW — not in original code) |
| **Analytics** | Aggregated stats generated from all saved responses (NEW — not in original code) |

---

## What's New vs. Original Code

| Feature | Original Code | Refactored Design |
|---------|--------------|-------------------|
| Structure | Flat script, no functions | OOP with 7 classes |
| Data persistence | None (answers lost on exit) | Save to CSV/JSON |
| Analytics | None | Response distributions, popular picks, summary reports |
| Input validation | Inline while loops | Encapsulated in Question class |
| Reusability | Copy-paste to change | Modular — swap questions, storage format, etc. |
| Testability | Not testable | Each class testable independently |

---

## Next Steps

1. ✅ Design phase — UML Class Diagram + Sequence Diagram (this document)
2. ⬜ Implement classes based on this design
3. ⬜ Add data persistence (CSV/JSON storage)
4. ⬜ Build analytics module
5. ⬜ Write unit tests
6. ⬜ Create user documentation
