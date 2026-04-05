# F1 Survey Analytics — Planning Document

## Background

CTHS (school) wants to understand the level of **awareness, interest, and preferences** around Formula 1 (F1) motorsport among its students. Currently, teachers have **no clarity** on:

- How many students know about F1
- What teams and drivers students prefer
- Whether there is enough interest to justify organising an F1-themed event

## The Ask

The school has asked students to:

1. **Build a survey program** in Python
2. **Run the survey** across classmates to collect responses
3. **Analyse the data** and report back with findings
4. **Present analytics** that help CTHS decide whether to organise an F1 event and what it should focus on

## Problem Statement

> There is no data on F1 awareness or preferences among CTHS students. The school needs a structured way to capture student opinions and generate actionable insights to plan a potential F1-themed event.

## Goals

### Goal 1: Capture Individual Survey Responses

Build a program that collects **opinion-based** responses from each student. There are **no right or wrong answers** — this is a preference survey, not a quiz.

**What we capture per student:**

| Category | Questions Cover |
|----------|----------------|
| **Awareness** | How much do they know about F1? How long have they watched? How many seasons? |
| **Team Preferences** | Favourite high-performing team, favourite mid-performing team, dream team to drive for |
| **Driver Preferences** | Which legendary F1 driver they'd pick to race with |
| **Viewing Preferences** | Where they'd go to watch a race (region) |
| **Future Predictions** | Which team they think will dominate in future |
| **Interest Level** | Overall interest in F1 (rarely, somewhat, fully, never) |

### Goal 2: Generate Analytics

The survey is not just about individual responses — it must produce **aggregated analytics** across all students. This is the data CTHS needs to make decisions.

**Analytics we need to produce:**

| Analytic | What It Tells CTHS |
|----------|-------------------|
| **Awareness Distribution** | What % of students have zero, little, some, or a lot of F1 knowledge |
| **Interest Level Breakdown** | How many students are fully interested vs never interested |
| **Most Popular Teams** | Which teams are most liked — helps plan event themes (e.g., Ferrari-themed decor) |
| **Most Popular Drivers** | Which legendary drivers students admire — useful for trivia or poster displays |
| **Preferred Race Regions** | Where students would travel to watch — could shape event activities (e.g., virtual race in a specific region) |
| **Future Predictions** | Which team students think will dominate — good for debate/discussion activities |
| **Watch History** | How many seasons students have watched — segments casual fans vs dedicated fans |

### Goal 3: Support CTHS Event Planning

The analytics output should give CTHS enough information to:

- **Decide** if there's sufficient student interest to run an F1 event
- **Theme** the event around the most popular teams and drivers
- **Segment** activities for casual fans vs hardcore fans
- **Engage** students by reflecting their own preferences back to them

## What This Program Is NOT

- ❌ Not a quiz — there are no correct answers
- ❌ Not graded — students aren't scored on their responses
- ❌ Not one-time — the program should handle multiple students taking the survey
- ❌ Not just data collection — analytics are equally important as capturing responses

## Success Criteria

| # | Criteria | How We Know It's Done |
|---|----------|----------------------|
| 1 | Any student in class 11SEG261 can take the survey | Class code authentication works |
| 2 | All 10 questions are answered with valid responses | Input validation rejects invalid answers |
| 3 | Individual results are shown back to the student | Results display after survey completion |
| 4 | Responses are saved and not lost | Data persists to file after submission |
| 5 | Analytics are generated from all collected responses | Summary report shows distributions and popular picks |
| 6 | CTHS can use the output to plan an event | Analytics answer: "Is there interest?" and "What do students like?" |

## Survey Flow

```
Student launches program
    → Enters name + class code
    → Authenticated? 
        No  → Access denied, exit
        Yes → Menu: Continue / Quit / Restart
            → Continue → 10 questions (A/B/C/D)
                → Review answers
                → Happy? 
                    Yes → Save to file → Show analytics → Exit
                    No  → Redo survey
            → Quit → Exit
            → Restart → Back to menu
```

## Data Flow

```
Individual Student          All Students Combined
─────────────────          ─────────────────────
Takes survey               Responses stored in file
    ↓                              ↓
Answers 10 Qs              Analytics engine reads all responses
    ↓                              ↓
Sees own results           Generates:
    ↓                        • Awareness distribution
Confirms & saves             • Team popularity rankings
                             • Driver popularity rankings
                             • Interest level breakdown
                             • Regional preferences
                                   ↓
                             CTHS uses for event planning
```

## Stakeholders

| Who | Role | Interest |
|-----|------|----------|
| **Students (11SEG261)** | Survey participants | Take the survey, see their results |
| **Ahan Kesharwani** | Developer | Build the program, demonstrate Python skills |
| **Teachers / CTHS** | Decision makers | Use analytics to decide on F1 event |

## Next Steps

1. ✅ Planning — goals, intent, success criteria (this document)
2. ✅ Design — UML class diagram + sequence diagram (see [DESIGN.md](DESIGN.md))
3. ⬜ Implementation — build the classes in Python
4. ⬜ Testing — verify survey flow + analytics output
5. ⬜ Deployment — run survey with classmates, collect real data
