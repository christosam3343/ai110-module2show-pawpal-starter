from datetime import date
from typing import Optional

import pytest

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion() -> None:
    task = Task("Morning Walk", 30, "high", "daily")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition() -> None:
    pet = Pet("Biscuit", "Golden Retriever", 3)
    initial_count = len(pet.tasks)
    task = Task("Breakfast", 10, "high", "daily")

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert task in pet.tasks


def test_sort_by_time() -> None:
    owner = Owner("John", 90)
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    late = Task("Grooming", 20, "medium", "daily", time="14:30")
    early = Task("Feeding", 15, "high", "daily", time="08:05")
    middle = Task("Walk", 30, "high", "daily", time="09:00")
    biscuit.add_task(late)
    biscuit.add_task(early)
    luna.add_task(middle)
    scheduler = Scheduler(owner)

    result = scheduler.sort_by_time()

    assert result == [early, middle, late]
    assert scheduler.sort_tasks() == result
    assert owner.pets == [biscuit, luna]
    assert biscuit.tasks == [late, early]
    assert luna.tasks == [middle]
    assert owner.get_all_tasks() == [late, early, middle]


def test_sort_keeps_untimed_tasks_last_and_preserves_ties() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    untimed_first = Task("Play", 10, "low", "daily")
    untimed_second = Task("Brush", 10, "low", "daily")
    timed_first = Task("Walk", 30, "high", "daily", time="08:00")
    timed_second = Task("Feed", 10, "high", "daily", time="08:00")
    for task in [untimed_first, timed_first, untimed_second, timed_second]:
        pet.add_task(task)

    result = Scheduler(owner).sort_by_time()

    assert result == [timed_first, timed_second, untimed_first, untimed_second]
    assert result is not pet.tasks
    assert pet.tasks == [untimed_first, timed_first, untimed_second, timed_second]


@pytest.mark.parametrize("time", ["25:00", "09:60", "9:00", "09:0", "12:00:00", "", "noon"])
def test_invalid_task_times(time: str) -> None:
    with pytest.raises(ValueError):
        Task("Walk", 30, "high", "daily", time=time)


@pytest.mark.parametrize("time", ["00:00", "23:59"])
def test_valid_boundary_times(time: str) -> None:
    task = Task("Care", 10, "high", "daily", time=time)

    assert task.time == time


def test_update_task_time() -> None:
    task = Task("Walk", 30, "high", "daily")
    task.update_task(time="09:30")
    assert task.time == "09:30"
    assert "Time: 09:30" in task.get_details()

    with pytest.raises(ValueError):
        task.update_task(name="Invalid update", time="25:00")

    assert task.name == "Walk"
    assert task.time == "09:30"


def test_filter_tasks_by_pet_name() -> None:
    owner = Owner("John", 90)
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    # These have equal field values but belong to different pets.
    biscuit_task = Task("Feeding", 10, "high", "daily")
    luna_task = Task("Feeding", 10, "high", "daily")
    biscuit.add_task(biscuit_task)
    luna.add_task(luna_task)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(pet_name="Biscuit")

    assert len(result) == 1
    assert result[0] is biscuit_task
    assert result is not biscuit.tasks
    assert scheduler.filter_tasks(pet_name="Unknown") == []
    assert len(owner.get_all_tasks()) == 2


def test_pet_name_filter_includes_all_pets_with_that_name() -> None:
    owner = Owner("John", 90)
    first_pet = Pet("Mochi", "Labrador", 3)
    second_pet = Pet("Mochi", "Persian Cat", 2)
    first_task = Task("Walk", 30, "high", "daily")
    second_task = Task("Groom", 20, "medium", "daily")
    first_pet.add_task(first_task)
    second_pet.add_task(second_task)
    owner.add_pet(first_pet)
    owner.add_pet(second_pet)

    assert Scheduler(owner).filter_tasks(pet_name="Mochi") == [first_task, second_task]


@pytest.mark.parametrize("completed", [True, False])
def test_filter_tasks_by_completion_status(completed: bool) -> None:
    owner = Owner("John", 90)
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    finished = Task("Breakfast", 10, "high", "daily")
    finished.mark_complete()
    pending = Task("Grooming", 20, "medium", "daily")
    biscuit.add_task(finished)
    luna.add_task(pending)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(completed=completed)

    assert result == ([finished] if completed else [pending])
    assert owner.get_all_tasks() == [finished, pending]
    assert scheduler.filter_tasks(pet_name="Biscuit", completed=False) == []
    assert scheduler.filter_tasks(pet_name="Luna", completed=False) == [pending]


@pytest.mark.parametrize(
    "frequency, expected_due_date",
    [("daily", date(2026, 10, 25)), ("weekly", date(2026, 10, 31))],
)
def test_recurring_task_due_date(frequency: str, expected_due_date: date) -> None:
    pet = Pet("Biscuit", "Golden Retriever", 3)
    task = Task("Care", 10, "high", frequency, due_date=date(2026, 10, 1))
    pet.add_task(task)

    next_task = pet.complete_task(task, completion_date=date(2026, 10, 24))

    assert next_task is not None
    assert next_task.due_date == expected_due_date
    assert next_task.completed is False
    assert task.completed is True
    assert pet.tasks[0] is task and pet.tasks[1] is next_task


@pytest.mark.parametrize(
    "frequency, completion_date, expected_due_date",
    [
        ("daily", date(2026, 1, 31), date(2026, 2, 1)),
        ("daily", date(2026, 12, 31), date(2027, 1, 1)),
        ("weekly", date(2026, 12, 28), date(2027, 1, 4)),
        ("daily", date(2028, 2, 28), date(2028, 2, 29)),
    ],
)
def test_recurring_task_date_rollover(
    frequency: str, completion_date: date, expected_due_date: date
) -> None:
    pet = Pet("Luna", "Persian Cat", 2)
    task = Task("Care", 15, "high", frequency)
    pet.add_task(task)

    next_task = pet.complete_task(task, completion_date=completion_date)

    assert next_task is not None
    assert next_task.due_date == expected_due_date


def test_recurrence_copies_details_and_keeps_correct_pet() -> None:
    owner = Owner("John", 90)
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    original = Task("Feeding", 15, "high", "daily", "Breakfast portion", time="07:30")
    other_task = Task("Feeding", 15, "high", "daily", "Breakfast portion", time="07:30")
    biscuit.add_task(original)
    luna.add_task(other_task)

    next_task = biscuit.complete_task(original, completion_date=date(2026, 10, 24))

    assert next_task is not None and next_task is not original
    assert next_task.name == original.name
    assert next_task.duration == original.duration
    assert next_task.priority == original.priority
    assert next_task.frequency == original.frequency
    assert next_task.description == original.description
    assert next_task.time == original.time
    assert next_task.completed is False
    assert biscuit.tasks[0] is original and biscuit.tasks[1] is next_task
    assert len(luna.tasks) == 1 and luna.tasks[0] is other_task
    assert other_task.completed is False
    assert len(Scheduler(owner).get_tasks()) == 3


def test_completing_same_task_does_not_duplicate_recurrence() -> None:
    pet = Pet("Biscuit", "Golden Retriever", 3)
    task = Task("Breakfast", 10, "high", "daily")
    pet.add_task(task)

    next_task = pet.complete_task(task, completion_date=date(2026, 10, 24))
    repeated_result = pet.complete_task(task, completion_date=date(2026, 10, 25))
    task.mark_incomplete()
    reopened_result = pet.complete_task(task, completion_date=date(2026, 10, 26))

    assert repeated_result is None and reopened_result is None
    assert len(pet.tasks) == 2
    assert pet.tasks[1] is next_task
    assert next_task.due_date == date(2026, 10, 25)
    assert task.completed is True


def test_next_occurrence_can_create_its_own_successor() -> None:
    pet = Pet("Biscuit", "Golden Retriever", 3)
    original = Task("Breakfast", 10, "high", "daily")
    pet.add_task(original)
    next_task = pet.complete_task(original, completion_date=date(2026, 10, 24))
    assert next_task is not None

    following_task = pet.complete_task(next_task, completion_date=date(2026, 10, 25))

    assert following_task is not None
    assert following_task.due_date == date(2026, 10, 26)
    assert following_task.completed is False
    assert next_task.completed is True
    assert len(pet.tasks) == 3


@pytest.mark.parametrize("frequency", ["once", "one-time"])
def test_non_recurring_task_does_not_create_successor(frequency: str) -> None:
    pet = Pet("Luna", "Persian Cat", 2)
    task = Task("Vet visit", 30, "high", frequency)
    pet.add_task(task)

    result = pet.complete_task(task, completion_date=date(2026, 10, 24))

    assert result is None
    assert task.completed is True
    assert len(pet.tasks) == 1 and pet.tasks[0] is task


def test_complete_task_rejects_another_pets_task() -> None:
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    task = Task("Feeding", 15, "high", "daily")
    equal_looking_task = Task("Feeding", 15, "high", "daily")
    biscuit.add_task(task)
    luna.add_task(equal_looking_task)

    with pytest.raises(ValueError, match="does not belong"):
        luna.complete_task(task, completion_date=date(2026, 10, 24))

    assert task.completed is False and equal_looking_task.completed is False
    assert len(biscuit.tasks) == 1 and len(luna.tasks) == 1


def test_task_only_completion_remains_status_only() -> None:
    pet = Pet("Biscuit", "Golden Retriever", 3)
    task = Task("Walk", 30, "high", "daily")
    pet.add_task(task)

    task.mark_complete()

    assert task.completed is True
    assert len(pet.tasks) == 1


def test_optional_due_date_preserves_constructor_and_supports_updates() -> None:
    task = Task("Walk", 30, "high", "daily", "Morning route", False, "09:00")
    assert task.due_date is None

    task.update_task(due_date=date(2026, 10, 24))

    assert task.due_date == date(2026, 10, 24)
    assert "Due date: 2026-10-24" in task.get_details()


def test_scheduler_handles_empty_task_lists() -> None:
    owner = Owner("John", 90)
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks() == []

    owner.add_pet(Pet("Biscuit", "Golden Retriever", 3))

    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks(pet_name="Biscuit", completed=False) == []


def test_conflicts_detect_exact_start_time_for_same_pet() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    walk = Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24))
    feeding = Task("Feeding", 10, "high", "once", time="09:00", due_date=date(2026, 10, 24))
    pet.add_task(walk)
    pet.add_task(feeding)

    warnings = Scheduler(owner).detect_conflicts()

    assert warnings == [
        "Warning: Conflict on 2026-10-24: Biscuit - Walk (09:00, 30 minutes) "
        "overlaps Biscuit - Feeding (09:00, 10 minutes)."
    ]
    assert pet.tasks == [walk, feeding]
    assert walk.completed is False and feeding.completed is False
    assert walk.time == "09:00" and feeding.time == "09:00"


def test_conflicts_detect_partial_overlap_across_pets() -> None:
    owner = Owner("John", 90)
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    biscuit.add_task(Task("Morning Walk", 30, "high", "daily", time="09:00", due_date=date(2026, 10, 24)))
    luna.add_task(Task("Playtime", 20, "low", "once", time="09:15", due_date=date(2026, 10, 24)))

    warnings = Scheduler(owner).detect_conflicts()

    assert warnings == [
        "Warning: Conflict on 2026-10-24: Biscuit - Morning Walk (09:00, 30 minutes) "
        "overlaps Luna - Playtime (09:15, 20 minutes)."
    ]


def test_back_to_back_tasks_are_not_conflicts() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    # Add the later task first to also check independence from insertion order.
    pet.add_task(Task("Breakfast", 10, "high", "once", time="09:30", due_date=date(2026, 10, 24)))
    pet.add_task(Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24)))

    assert Scheduler(owner).detect_conflicts() == []


def test_tasks_on_different_dates_are_not_conflicts() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Walk today", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24)))
    pet.add_task(Task("Walk tomorrow", 30, "high", "once", time="09:00", due_date=date(2026, 10, 25)))

    assert Scheduler(owner).detect_conflicts() == []


@pytest.mark.parametrize(
    "due_date, time",
    [(None, None), (None, "09:00"), (date(2026, 10, 24), None)],
)
def test_unscheduled_tasks_are_excluded_from_conflict_check(
    due_date: Optional[date], time: Optional[str]
) -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    scheduled = Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24))
    unscheduled = Task("Unscheduled care", 20, "medium", "once", time=time, due_date=due_date)
    pet.add_task(scheduled)
    pet.add_task(unscheduled)

    assert Scheduler(owner).detect_conflicts() == []
    assert pet.tasks == [scheduled, unscheduled]


def test_completed_tasks_are_excluded_from_conflict_check() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    finished = Task("Breakfast", 10, "high", "once", time="09:00", due_date=date(2026, 10, 24))
    finished.mark_complete()
    pet.add_task(finished)
    pet.add_task(Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24)))

    assert Scheduler(owner).detect_conflicts() == []


def test_conflict_check_handles_empty_single_and_non_overlapping_tasks() -> None:
    owner = Owner("John", 90)
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    assert scheduler.detect_conflicts() == []
    pet.add_task(Task("Breakfast", 10, "high", "once", time="08:00", due_date=date(2026, 10, 24)))
    assert scheduler.detect_conflicts() == []
    pet.add_task(Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24)))

    assert scheduler.detect_conflicts() == []


def test_conflict_pairs_are_reported_only_once() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    for name in ["Task A", "Task B", "Task C"]:
        pet.add_task(Task(name, 10, "high", "once", time="09:00", due_date=date(2026, 10, 24)))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 3
    for first_name, second_name in [("Task A", "Task B"), ("Task A", "Task C"), ("Task B", "Task C")]:
        assert sum(first_name in warning and second_name in warning for warning in warnings) == 1


def test_equal_looking_tasks_keep_correct_pet_names_in_warning() -> None:
    owner = Owner("John", 90)
    biscuit = Pet("Biscuit", "Golden Retriever", 3)
    luna = Pet("Luna", "Persian Cat", 2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    biscuit.add_task(Task("Feeding", 10, "high", "once", time="09:00", due_date=date(2026, 10, 24)))
    luna.add_task(Task("Feeding", 10, "high", "once", time="09:00", due_date=date(2026, 10, 24)))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "Biscuit - Feeding" in warnings[0]
    assert "Luna - Feeding" in warnings[0]


def test_repeated_task_reference_does_not_duplicate_warnings() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    walk = Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24))
    pet.add_task(walk)
    pet.add_task(walk)
    pet.add_task(Task("Feeding", 10, "high", "once", time="09:00", due_date=date(2026, 10, 24)))

    assert len(Scheduler(owner).detect_conflicts()) == 1


def test_zero_duration_task_does_not_occupy_time() -> None:
    owner = Owner("John", 90)
    pet = Pet("Biscuit", "Golden Retriever", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, "high", "once", time="09:00", due_date=date(2026, 10, 24)))
    pet.add_task(Task("Reminder", 0, "low", "once", time="09:15", due_date=date(2026, 10, 24)))

    assert Scheduler(owner).detect_conflicts() == []
