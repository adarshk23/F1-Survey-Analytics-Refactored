# F1 Survey Analytics — Product Specification

> Derived from [REQUIREMENTS.md](REQUIREMENTS.md) | See also [DESIGN.md](DESIGN.md)

---

## 1. Product Summary

**F1 Survey Analytics** is a Python console application that allows CTHS students to participate in a 10-question Formula 1 preference survey. The program captures individual responses, persists them to file, and generates aggregated analytics to help CTHS teachers decide whether to organise an F1-themed school event.

---

## 2. Users

| User Type | Description | Interaction |
|-----------|-------------|-------------|
| **Student** | Year 11 student in class 11SEG261 | Takes the survey, reviews their answers |
| **Teacher / Admin** | CTHS staff reviewing results | Views analytics output to make event decisions |

---

## 3. Functional Specifications

### 3.1 Authentication

| ID | Spec | Details |
|----|------|---------|
| AUTH-01 | Program prompts for student name | Free text input, required |
| AUTH-02 | Program prompts for class code | Free text input, required |
| AUTH-03 | Class code validated against `11SEG261` | Case-sensitive match |
| AUTH-04 | Invalid class code → access denied message | Program exits, does NOT reveal correct code |
| AUTH-05 | Valid class code → proceed to main menu | Student welcomed by name |

### 3.2 Main Menu

| ID | Spec | Details |
|----|------|---------|
| MENU-01 | Display 3 options: Continue, Quit, Restart | Numbered 1, 2, 3 |
| MENU-02 | Option 1 (Continue) → launch survey | Proceeds to survey questions |
| MENU-03 | Option 2 (Quit) → exit program | Displays goodbye message, terminates |
| MENU-04 | Option 3 (Restart) → return to menu | Loops back to menu display |
| MENU-05 | Invalid input → error message | Prompts user to re-enter 1, 2, or 3 |

### 3.3 Survey Questions

10 multiple-choice questions, each with 4 options (A, B, C, D). No correct answers — all are preference-based.

| Q# | Category | Question | Options |
|----|----------|----------|---------|
| 1 | Awareness | How much knowledge do you hold about F1? | A) Zero, B) Little, C) Some, D) A lot |
| 2 | Watch History | How long have you watched F1? | A) 0-1 Years, B) 1-3 Years, C) 3-5 Years, D) 5+ Years |
| 3 | Watch History | How many full seasons have you watched? | A) None, B) 1, C) 2-3, D) Greater than 3 |
| 4 | Team Pref | What high performing team would you go for? | A) McLaren, B) Ferrari, C) Mercedes, D) Red Bull |
| 5 | Team Pref | What middle performing team would you go for? | A) Williams, B) Haas, C) Aston Martin, D) Alpine |
| 6 | Viewing Pref | Where would you go and watch an F1 race? | A) Asia/SE Asia, B) Europe, C) South America, D) Middle East |
| 7 | Prediction | Which team will dominate in the future? | A) Red Bull, B) Mercedes, C) Ferrari, D) Audi |
| 8 | Driver Pref | Which legendary F1 driver would you pick? | A) Ayrton Senna, B) Michael Schumacher, C) Nigel Mansell, D) Damon Hill |
| 9 | Team Pref | If you had to drive for an F1 Team, what would it be? | A) Mercedes, B) Williams, C) Ferrari, D) McLaren |
| 10 | Interest | Do you show interest in F1? | A) Yes (Rarely), B) Yes (Somewhat), C) Yes (Fully), D) Never |

### 3.4 Input Validation

| ID | Spec | Details |
|----|------|---------|
| VAL-01 | Only A, B, C, D accepted for survey answers | Case-insensitive (auto-converted to uppercase) |
| VAL-02 | Invalid answer → error message + re-prompt | Loop until valid input received |
| VAL-03 | Only 1, 2, 3 accepted for menu choices | Invalid → error message + re-prompt |
| VAL-04 | Only Y, N accepted for confirmation | Case-insensitive, invalid → re-prompt |

### 3.5 Results Display

| ID | Spec | Details |
|----|------|---------|
| RES-01 | After survey, display all 10 Q&A pairs | Question text + student's answer |
| RES-02 | Formatted with clear headings | "FINAL SURVEY RESULTS" header |
| RES-03 | Confirmation prompt after results | "Are you happy with your answers? (Y/N)" |
| RES-04 | Confirm Y → save and exit | Responses saved to file |
| RES-05 | Confirm N → return to menu | Student can redo the survey |

### 3.6 Data Persistence

| ID | Spec | Details |
|----|------|---------|
| DATA-01 | Save each submission to a file | CSV or JSON format |
| DATA-02 | Each record includes: student name, class code, timestamp, 10 answers | One row per submission |
| DATA-03 | File appends (does not overwrite) | Multiple students' data accumulates |
| DATA-04 | File created automatically if it doesn't exist | No manual setup required |
| DATA-05 | Data survives program restart | Persistent storage on disk |

**CSV Record Format:**

```
name, class_code, timestamp, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10
"Ahan Kesharwani", "11SEG261", "2026-04-05 11:30:00", "C", "D", "B", "B", "C", "A", "C", "A", "C", "C"
```

### 3.7 Analytics

| ID | Spec | Details |
|----|------|---------|
| ANA-01 | Total number of survey respondents | Count of all saved records |
| ANA-02 | Response distribution per question | Count + percentage for each option (A/B/C/D) |
| ANA-03 | Most popular answer per question | The option with highest count |
| ANA-04 | Awareness summary | % breakdown of Q1 (Zero / Little / Some / A lot) |
| ANA-05 | Interest level summary | % breakdown of Q10 (Rarely / Somewhat / Fully / Never) |
| ANA-06 | Top team rankings | Combined popularity from Q4, Q5, Q9 |
| ANA-07 | Top driver ranking | Most picked legendary driver from Q8 |
| ANA-08 | Preferred race region | Most popular viewing location from Q6 |
| ANA-09 | Analytics displayed in console | Formatted text output with tables/bars |
| ANA-10 | Analytics available after each submission | Auto-generated from all stored data |

**Example Analytics Output:**

```
═══════════════════════════════════════
        F1 SURVEY ANALYTICS REPORT
        Total Respondents: 25
═══════════════════════════════════════

AWARENESS LEVEL (Q1):
  Zero    ████░░░░░░░░░░░░░░░░  16% (4)
  Little  ████████░░░░░░░░░░░░  32% (8)
  Some    ██████████░░░░░░░░░░  36% (9)
  A lot   ████░░░░░░░░░░░░░░░░  16% (4)

MOST POPULAR HIGH-PERFORMING TEAM (Q4):
  1. Ferrari     ██████████████░░░░░░  44% (11)
  2. Red Bull    ████████░░░░░░░░░░░░  28% (7)
  3. McLaren     ████░░░░░░░░░░░░░░░░  16% (4)
  4. Mercedes    ███░░░░░░░░░░░░░░░░░  12% (3)

INTEREST LEVEL (Q10):
  Fully     ████████████░░░░░░░░  48% (12)
  Somewhat  ████████░░░░░░░░░░░░  28% (7)
  Rarely    ████░░░░░░░░░░░░░░░░  16% (4)
  Never     ██░░░░░░░░░░░░░░░░░░   8% (2)

HEADLINE: 92% of students show some level of F1 interest.
RECOMMENDATION: Sufficient interest to proceed with F1 event.
```

---

## 4. Non-Functional Specifications

| ID | Spec | Details |
|----|------|---------|
| NF-01 | Written in Python 3 | No external libraries required for core functionality |
| NF-02 | Runs in terminal/console | No GUI required |
| NF-03 | Object-Oriented design | Classes as defined in DESIGN.md |
| NF-04 | Code commented | Clear comments explaining logic (school assessment requirement) |
| NF-05 | Handles edge cases gracefully | Empty files, no previous data, single respondent |
| NF-06 | Works on school computers | Standard Python install, no pip dependencies |

---

## 5. Out of Scope (v1)

- Web interface or GUI
- Database storage (file-based only)
- Email or export of analytics report
- Multi-class support (11SEG261 only for now)
- Chart images (text-based bar charts only)

---

## 6. File Structure

```
F1-Survey-Analytics-Refactored/
├── REQUIREMENTS.md          ← Why we're building this
├── SPEC.md                  ← What we're building (this document)
├── DESIGN.md                ← How we're building it (UML diagrams)
├── README.md                ← Project overview
├── original/
│   └── survey_original.py   ← Original code (reference)
├── src/
│   ├── main.py              ← Entry point
│   ├── app.py               ← SurveyApp class
│   ├── auth.py              ← Authenticator + User classes
│   ├── survey.py            ← Survey + Question classes
│   ├── storage.py           ← DataStorage class
│   └── analytics.py         ← Analytics class
├── data/
│   └── responses.csv        ← Saved survey responses
└── tests/
    └── test_survey.py       ← Unit tests
```

---

## 7. Traceability Matrix

Maps each requirement goal to its spec IDs:

| Requirement Goal | Spec IDs |
|-----------------|----------|
| Goal 1: Capture Responses | AUTH-01→05, MENU-01→05, VAL-01→04, RES-01→05 |
| Goal 2: Generate Analytics | DATA-01→05, ANA-01→10 |
| Goal 3: Support Event Planning | ANA-04→08 (awareness, interest, teams, drivers, regions) |
