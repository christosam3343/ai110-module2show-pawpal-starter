# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Implementation Summary

The core Python classes now support pet care task management. `Owner` stores owner information and a list of multiple `Pet` objects. Each `Pet` stores its information and manages its own `Task` objects through methods to add, remove, and retrieve tasks. Tasks include descriptions, durations in minutes, priorities, frequency, and completion status, with methods to update their information and mark them complete or incomplete.

`Owner.get_all_tasks()` combines the tasks from every pet. `Scheduler` accesses that combined list through the owner, so it includes tasks for all pets. `main.py` demonstrates this with John, Biscuit, Luna, and five initial care tasks, followed by sorting, filtering, recurring occurrences, and an overlap warning.

The original two pytest tests check task completion and task addition. The expanded suite also covers time validation, sorting, filtering, daily and weekly recurrence, and conflict detection. The Streamlit interface now records pets and tasks in a session-state Owner. Its scheduling control remains disabled; the implemented scheduling features are demonstrated through the backend and CLI.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run `python main.py` in the project's virtual environment to see the current multi-pet demonstration. It uses a fixed completion date for repeatable output and manually entered task times; it does not automatically build or rearrange a plan.

```text
Today's Schedule - PawPal+
Owner: John
Times are entered manually; overlap warnings do not move tasks.

Biscuit (Golden Retriever)
- 09:00 | Biscuit | Morning Walk | 30 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete
- 08:00 | Biscuit | Breakfast | 10 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete

Luna (Persian Cat)
- 07:30 | Luna | Feeding | 15 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete
- 10:00 | Luna | Grooming | 20 minutes | Priority: medium | Due: 2026-10-24 | Status: incomplete
- 09:15 | Luna | Playtime | 20 minutes | Priority: low | Due: 2026-10-24 | Status: incomplete

All pets - sorted by time
- 07:30 | Luna | Feeding | 15 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete
- 08:00 | Biscuit | Breakfast | 10 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete
- 09:00 | Biscuit | Morning Walk | 30 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete
- 09:15 | Luna | Playtime | 20 minutes | Priority: low | Due: 2026-10-24 | Status: incomplete
- 10:00 | Luna | Grooming | 20 minutes | Priority: medium | Due: 2026-10-24 | Status: incomplete

Biscuit - incomplete tasks
- 09:00 | Biscuit | Morning Walk | 30 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete
- 08:00 | Biscuit | Breakfast | 10 minutes | Priority: high | Due: 2026-10-24 | Status: incomplete

Recurring task completion demo - completed on 2026-10-24

Biscuit - daily: completed original (kept in pet's task list)
- 08:00 | Biscuit | Breakfast | 10 minutes | Priority: high | Due: 2026-10-24 | Status: completed
New incomplete occurrence:
- 08:00 | Biscuit | Breakfast | 10 minutes | Priority: high | Due: 2026-10-25 | Status: incomplete

Luna - weekly: completed original (kept in pet's task list)
- 10:00 | Luna | Grooming | 20 minutes | Priority: medium | Due: 2026-10-24 | Status: completed
New incomplete occurrence:
- 10:00 | Luna | Grooming | 20 minutes | Priority: medium | Due: 2026-10-31 | Status: incomplete

Conflict check - incomplete tasks with a due date and clock time
Tasks missing a due date or clock time are unscheduled and were not checked.
Warning: Conflict on 2026-10-24: Biscuit - Morning Walk (09:00, 30 minutes) overlaps Luna - Playtime (09:15, 20 minutes).
```

## Testing PawPal+

Run the full test suite from the project root with the virtual environment active:

```bash
python -m pytest
```

The suite covers task completion and addition, time validation, chronological sorting, pet/status filtering, multi-pet task retrieval, daily and weekly recurrence, calendar rollover, and duplicate prevention. Conflict tests cover exact matches, partial and fully contained overlaps, back-to-back tasks, and exclusion of completed or unscheduled tasks. The three new regression tests also check re-sorting after a time update without changing stored order and finding a pet added after Scheduler creation.

Actual successful terminal output:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\OneDrive - University of New Haven\School Files - UNH\Sem 4\Codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 49 items

tests\test_pawpal.py .................................................   [100%]

============================= 49 passed in 0.21s ==============================
```

**Confidence Level: 4/5 stars (★★★★☆).** The main backend behaviors have automated coverage. Overnight conflicts across different due dates and full UI scheduling remain outside the implemented behavior; the Streamlit Generate schedule control is still disabled.

## Smarter Scheduling

The Scheduler methods below retrieve tasks across all pets through `Owner.get_all_tasks()`. Recurrence is handled by the pet that owns the task.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Time sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_tasks()` | Return a new list ordered by validated `HH:MM` clock times. Untimed tasks go last; equal times and untimed tasks retain their original order. Sorting does not change stored lists or order tasks by due date. |
| Pet/status filtering | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Filter by exact pet name, completion status, or both. A shared name includes every matching pet. `completed=False` selects incomplete tasks; `None` leaves that filter off. |
| Recurring tasks | `Pet.complete_task(task, completion_date=None)` | Complete a task belonging to that pet and append one incomplete successor: daily tasks are due 1 day after completion, weekly tasks 7 days after completion. Copy task details and clock time, preserve the original, and prevent duplicate successors. Omitted completion dates use today. Other frequencies create no successor. |
| Overlap warnings | `Scheduler.detect_conflicts()` | Return warning messages for incomplete tasks with overlapping start times and durations on the same due date, including tasks for different pets. Back-to-back tasks are allowed, each pair is reported once, and no conflicts returns an empty list. |

Use `Pet.complete_task()` to trigger recurrence; `Task.mark_complete()` and `Task.mark_completed()` only change completion status. The next occurrence is already stored on the same pet.

Conflict checks require a due date, clock time, and positive duration. Tasks missing a date or time are unscheduled and are not checked, so an empty warning list does not establish that those tasks are conflict-free. Overnight overlaps between different due dates are not detected. Priorities and available minutes are stored, but these methods do not automatically choose tasks to fit a time budget or move conflicting tasks.

The Streamlit **Generate schedule** control is still disabled, and `Scheduler.generate_schedule()` still raises `NotImplementedError`. Streamlit supports adding pets and recording tasks; the sorting, filtering, recurrence, and conflict workflows above are currently demonstrated in `main.py` and verified by pytest.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
