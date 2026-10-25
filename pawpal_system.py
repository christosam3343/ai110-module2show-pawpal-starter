"""Core pet care data and task management for PawPal+.

Task durations and owner/scheduler available time are measured in minutes.
Task priority levels are high, medium, and low.
Optional task times use zero-padded, 24-hour HH:MM format.
For task updates, None means to leave that field unchanged.
Pet.complete_task() creates daily or weekly successors; Task completion is status-only.
Sorting, filtering, recurrence, and overlap warnings are available; tasks are not automatically moved.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional


class Owner:
    def __init__(
        self,
        name: str,
        available_time: float,
        preferences: Optional[Dict[str, object]] = None,
    ) -> None:
        """Create an owner with available care time, preferences, and no pets yet."""
        if available_time < 0:
            raise ValueError("Available time cannot be negative.")
        self.name = name
        self.available_time = available_time
        self.preferences = preferences if preferences is not None else {}
        self.pets: List["Pet"] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def update_availability(self, time: float) -> None:
        """Update the owner's available care time in minutes."""
        if time < 0:
            raise ValueError("Available time cannot be negative.")
        self.available_time = time

    def get_all_tasks(self) -> List["Task"]:
        """Combine tasks from every pet, keeping pet and task order."""
        tasks: List["Task"] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


@dataclass
class Pet:
    name: str
    breed: str
    age: int
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task if it is present; otherwise leave the list unchanged."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List["Task"]:
        """Return a copy of the task list containing the same task objects."""
        return self.tasks.copy()

    def complete_task(
        self,
        task: "Task",
        completion_date: Optional[date] = None,
    ) -> Optional["Task"]:
        """Complete this pet's task and append at most one recurring successor.

        Daily and weekly successors are due 1 or 7 days after completion_date,
        which defaults to today. Return the new task, or None if none is created.
        Keep the original task; completing it again never adds another successor.
        """
        if not any(pet_task is task for pet_task in self.tasks):
            raise ValueError("This task does not belong to this pet.")

        # Each original task can create only one successor, even after reopening it.
        if task._next_occurrence_created:
            task.mark_complete()
            return None

        next_task = None
        if task.frequency in ("daily", "weekly"):
            if completion_date is None:
                completion_date = date.today()
            days = 1 if task.frequency == "daily" else 7
            next_task = Task(
                name=task.name,
                duration=task.duration,
                priority=task.priority,
                frequency=task.frequency,
                description=task.description,
                completed=False,
                time=task.time,
                due_date=completion_date + timedelta(days=days),
            )

        task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
            task._next_occurrence_created = True
        return next_task


@dataclass
class Task:
    name: str
    duration: float
    priority: str
    frequency: str
    description: str = ""
    completed: bool = False
    time: Optional[str] = None
    due_date: Optional[date] = None
    _next_occurrence_created: bool = field(default=False, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        """Check basic task values after the dataclass creates the task."""
        if self.duration < 0:
            raise ValueError("Task duration cannot be negative.")
        if self.priority not in ("high", "medium", "low"):
            raise ValueError("Priority must be high, medium, or low.")
        self._validate_time(self.time)

    @staticmethod
    def _validate_time(time: Optional[str]) -> None:
        """Accept None or a valid zero-padded, 24-hour HH:MM time."""
        if time is None:
            return
        if not isinstance(time, str) or len(time) != 5 or time[2] != ":":
            raise ValueError("Time must use 24-hour HH:MM format, such as 09:30.")
        hour = time[:2]
        minute = time[3:]
        if not (hour.isascii() and hour.isdigit() and minute.isascii() and minute.isdigit()):
            raise ValueError("Time must contain two hour digits and two minute digits.")
        if int(hour) > 23 or int(minute) > 59:
            raise ValueError("Time hours must be 00-23 and minutes must be 00-59.")

    def update_task(
        self,
        name: Optional[str] = None,
        duration: Optional[float] = None,
        priority: Optional[str] = None,
        frequency: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
        time: Optional[str] = None,
        due_date: Optional[date] = None,
    ) -> None:
        """Update supplied fields; None leaves a field unchanged."""
        # Validate first so an invalid update does not partially change the task.
        if duration is not None and duration < 0:
            raise ValueError("Task duration cannot be negative.")
        if priority is not None and priority not in ("high", "medium", "low"):
            raise ValueError("Priority must be high, medium, or low.")
        self._validate_time(time)

        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        if time is not None:
            self.time = time
        if due_date is not None:
            self.due_date = due_date

    def get_details(self) -> str:
        """Describe all task fields in a readable format."""
        status = "completed" if self.completed else "incomplete"
        return (
            f"{self.name}: {self.description} | "
            f"Time: {self.time if self.time is not None else 'not set'} | "
            f"Due date: {self.due_date.isoformat() if self.due_date is not None else 'not set'} | "
            f"Duration: {self.duration} minutes | Priority: {self.priority} | "
            f"Frequency: {self.frequency} | Status: {status}"
        )

    def mark_completed(self) -> None:
        """Set the task's completion status to True."""
        self.completed = True

    def mark_complete(self) -> None:
        """Mark this task complete without recurrence; use Pet.complete_task() for that."""
        self.mark_completed()

    def mark_incomplete(self) -> None:
        """Set the task's completion status to False."""
        self.completed = False


class Scheduler:
    """Retrieve, sort, filter, and check overlaps across an owner's pet tasks."""

    def __init__(self, owner: Owner) -> None:
        """Connect the scheduler to the owner whose pets need care."""
        self.owner = owner

    def get_tasks(self) -> List[Task]:
        """Retrieve current tasks from all pets through the owner."""
        return self.owner.get_all_tasks()

    @property
    def tasks(self) -> List[Task]:
        """Keep scheduler.tasks up to date when the owner's pets or tasks change."""
        return self.get_tasks()

    @property
    def available_time(self) -> float:
        """Read the owner's current available time in minutes."""
        return self.owner.available_time

    def sort_tasks(self) -> List[Task]:
        """Delegate to sort_by_time() while keeping the original method name."""
        return self.sort_by_time()

    def sort_by_time(self) -> List[Task]:
        """Return a new list sorted by clock time only, without changing stored lists.

        Due dates are not part of the sort. Equal times and untimed tasks keep
        their original order, with untimed tasks appearing last.
        """
        return sorted(self.get_tasks(), key=lambda task: (task.time is None, task.time or ""))

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Return a new list matching optional exact pet names and completion status.

        A shared name includes every matching pet. None disables that filter;
        completed=False selects incomplete tasks. Stored lists are unchanged.
        """
        tasks = self.get_tasks()
        if pet_name is not None:
            matching_pet_tasks: List[Task] = []
            for pet in self.owner.pets:
                if pet.name == pet_name:
                    matching_pet_tasks.extend(pet.get_tasks())
            # Compare identity so equal-looking tasks from other pets do not match.
            tasks = [
                task for task in tasks
                if any(task is pet_task for pet_task in matching_pet_tasks)
            ]
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return one warning per overlapping pair of incomplete tasks on the same date.

        Only tasks with a due date, clock time, and positive duration are checked.
        Missing dates or times mean unscheduled, not confirmed conflict-free.
        Back-to-back tasks are allowed. Overnight overlaps across dates are not
        detected, and tasks are never moved automatically.
        """
        scheduled_tasks = []
        for task in self.get_tasks():
            if task.completed or task.due_date is None or task.time is None:
                continue
            # A zero-duration task occupies no time.
            if task.duration <= 0:
                continue
            # Ignore repeated references to the same task object.
            if any(task is entry[1] for entry in scheduled_tasks):
                continue
            hour, minute = task.time.split(":")
            start = int(hour) * 60 + int(minute)
            end = start + task.duration
            for pet in self.owner.pets:
                if any(pet_task is task for pet_task in pet.tasks):
                    scheduled_tasks.append((pet.name, task, start, end))
                    break

        warnings: List[str] = []
        for index, (first_pet, first_task, first_start, first_end) in enumerate(scheduled_tasks):
            # Only compare with later entries so each pair is checked once.
            for second_pet, second_task, second_start, second_end in scheduled_tasks[index + 1:]:
                if first_task.due_date != second_task.due_date:
                    continue
                if first_start < second_end and second_start < first_end:
                    warnings.append(
                        f"Warning: Conflict on {first_task.due_date.isoformat()}: "
                        f"{first_pet} - {first_task.name} ({first_task.time}, {first_task.duration:g} minutes) "
                        f"overlaps {second_pet} - {second_task.name} "
                        f"({second_task.time}, {second_task.duration:g} minutes)."
                    )
        return warnings

    def generate_schedule(self) -> List[Task]:
        """Raise NotImplementedError because automatic plan generation is not implemented."""
        raise NotImplementedError("Schedule generation is reserved for Phase 4.")
