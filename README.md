# PawPal+ (Module 2 Project)

**PawPal+** is a Python and Streamlit application for managing pets and their care tasks. Enter task times, review the task list, check for overlaps, and complete daily or weekly tasks to create their next occurrences.

## Scenario

A busy pet owner needs a clear way to track feeding, walks, medication, grooming, and other care across multiple pets. PawPal+ records these activities and helps the owner review their timing. Task times are entered by the user; automatic schedule generation is not implemented, and **Generate schedule** remains disabled.

## Features

- Manage multiple pets with a name, breed, and age, under one owner.
- Add care tasks with a title, duration in minutes, high/medium/low priority, daily/weekly/once frequency, optional description, due date, and clock time.
- View tasks ordered by their entered clock times, with untimed tasks last. This order spans all due dates; it is not a dated calendar or an automatically generated daily plan.
- Filter by pet name and by All tasks, Incomplete, or Completed. A name filter includes every pet with that exact name; pet numbers distinguish individual pets when adding or completing tasks.
- Mark a task complete and keep the completed original. Daily and weekly tasks create one new incomplete occurrence for the same pet, due 1 or 7 days after the selected completion date. A once task creates no successor.
- See warnings for overlapping incomplete tasks on the same due date, including tasks belonging to different pets. Tasks are never moved or deleted to resolve a warning.
- Track completed and incomplete tasks in the overview, including the due dates of recurring occurrences.
- Keep the Owner, pets, and tasks in Streamlit session state across normal widget reruns. This is temporary session storage, not a file or database; it does not guarantee data survives a new session or server restart.

## Implementation Summary

The backend in `pawpal_system.py` uses four classes. `Owner` stores owner information and multiple `Pet` objects. Each `Pet` manages its own `Task` objects and handles recurring-task completion. `Task` stores the care details, optional time and due date, and completion status. `Scheduler` retrieves tasks through the Owner to sort, filter, and check overlaps. The backend also supports task updates and removal; the current UI provides task creation and completion controls.

`Owner.get_all_tasks()` combines the tasks from every pet. `Scheduler` accesses that combined list through the owner, so it includes tasks for all pets. `main.py` demonstrates this with John, Biscuit, Luna, and five initial care tasks, followed by sorting, filtering, recurring occurrences, and an overlap warning.

`app.py` connects the same backend to Streamlit forms, a filtered task table, completion controls, and conflict warnings. It keeps the Owner in session state and reads the current pet/task objects on reruns. The pytest suite checks the backend behaviors described below.

## Getting started

### Setup

Create the environment and install the dependencies from the project root. If the environment already exists, activate it and reuse it.

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install the dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. Keep that terminal running while using the application. To run the CLI demonstration instead, use `python main.py`.

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

The 49 test cases cover task completion and addition, time validation, chronological sorting, pet/status filtering, multi-pet task retrieval, daily and weekly recurrence, calendar rollover, and duplicate prevention. Conflict tests cover exact matches, partial and fully contained overlaps, back-to-back tasks, and exclusion of completed or unscheduled tasks. Regression tests also check re-sorting after a time update without changing stored order and finding a pet added after Scheduler creation.

Recorded successful backend test run:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\OneDrive - University of New Haven\School Files - UNH\Sem 4\Codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 49 items

tests\test_pawpal.py .................................................   [100%]

============================= 49 passed in 0.21s ==============================
```

**Confidence Level: 4/5 stars (★★★★☆).** The main backend behaviors have automated coverage. Streamlit AppTest also checked adding pets/tasks, sorting, filters, recurrence, conflict warnings, and rerun persistence. The conflict-warning and daily-recurrence flows were manually verified in the browser during Phase 6. Overnight conflicts across different due dates are not detected, and automatic plan generation remains unimplemented; **Generate schedule** is disabled.

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

The Streamlit interface now exposes sorting, pet/status filtering, recurring-task completion, and overlap warnings. Warnings always consider all pets' scheduled incomplete tasks, even when the displayed table is filtered. The **Generate schedule** control remains disabled, and `Scheduler.generate_schedule()` still raises `NotImplementedError`. Owner preferences and available minutes are stored by the backend but have no editing controls in this UI and are not used for automatic task selection.

## UML Documentation

The [final UML diagram source](diagrams/uml_final.mmd) documents the current fields, public methods, and relationships of Owner, Pet, Task, and Scheduler. It includes task time/due date, recurrence, sorting, filtering, and conflict warnings. The [draft UML](diagrams/uml_draft.mmd) is preserved to show how the design evolved.

## Demo Walkthrough

1. With the virtual environment active, run `python -m streamlit run app.py` from the project root and open the displayed local URL.
2. In **Owner and pets**, enter your name in **Owner name**. An empty name leaves the saved owner name unchanged.
3. In **Add a pet**, enter Biscuit, Golden Retriever, and age 3, then click **Add pet**. Repeat for Luna, Persian Cat, age 2. Both appear under **Your pets**.
4. In **Tasks**, select Biscuit in **Pet**. Enter Morning Walk as the **Task title**, 30 in **Duration (minutes)**, high **Priority**, and daily **Frequency**. Choose a **Due date (optional)** and **Start time (optional)** of 09:00, then click **Add task**. A description is optional. Leaving the date or time blank records an unscheduled task that cannot be checked for time conflicts.
5. Review **Care task overview**. Tasks appear by clock time across all dates, with untimed tasks last. Use **Pet name filter** and **Status filter** to narrow the table. If pets share a name, the name filter includes them all; the displayed pet numbers distinguish them.
6. Add Grooming for Luna with a duration of 20 minutes, medium priority, weekly frequency, the same due date as Morning Walk, and a start time of 09:15. The 09:00-09:30 walk overlaps the 09:15-09:35 grooming task. A warning near the overview names both pets and tasks, the date, and their times. It does not move either task, and it remains relevant even if the table is filtered.
7. In **Complete a task**, select Biscuit's Morning Walk in **Task to complete**, choose the same date in **Completion date**, and click **Mark complete**. The result table shows the completed original and a new incomplete occurrence due the next day at the same clock time. Use **All tasks** in **Status filter** to see both in the overview after later reruns.
8. Completing a weekly task through the same control creates its next occurrence 7 days after the selected completion date. Completing a once task does not create another occurrence. Repeating a normal rerun does not create extra successors.
9. Change a filter or the owner name to trigger a normal rerun and confirm your pets and tasks remain available. The data belongs to the current session. **Generate schedule** stays disabled because automatic plan generation is not implemented.
