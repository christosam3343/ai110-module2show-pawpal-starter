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

`Owner.get_all_tasks()` combines the tasks from every pet. `Scheduler` accesses that combined list through the owner, so it includes tasks for all pets. `main.py` demonstrates this with John, Biscuit, Luna, and four care tasks, printing a preliminary daily task preview.

The two pytest tests check that marking a task complete changes its status and that adding a task increases a pet's task count by one and stores the task. Advanced scheduling, including sorting, conflict detection, and recurring task handling, is reserved for Phase 4. Connecting the backend to the starter Streamlit interface will happen in a later phase.

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

Run `python main.py` in the project's virtual environment to see this preliminary daily task preview. Automatic scheduling will be implemented in Phase 4.

```text
Today's Schedule - PawPal+
Owner: John
Preliminary daily task preview (no automatic sorting or start times).

Biscuit (Golden Retriever)
- Morning Walk | 30 minutes | Priority: high | Status: incomplete
- Breakfast | 10 minutes | Priority: high | Status: incomplete

Luna (Persian Cat)
- Feeding | 15 minutes | Priority: high | Status: incomplete
- Grooming | 20 minutes | Priority: medium | Status: incomplete
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
