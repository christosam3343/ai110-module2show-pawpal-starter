"""Core pet care data and task management for PawPal+.

Task durations and owner/scheduler available time are measured in minutes.
Task priority levels are high, medium, and low.
For task updates, None means to leave that field unchanged.
Scheduling algorithms are reserved for Phase 4.
"""

from dataclasses import dataclass, field
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


@dataclass
class Task:
    name: str
    duration: float
    priority: str
    frequency: str
    description: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """Check basic task values after the dataclass creates the task."""
        if self.duration < 0:
            raise ValueError("Task duration cannot be negative.")
        if self.priority not in ("high", "medium", "low"):
            raise ValueError("Priority must be high, medium, or low.")

    def update_task(
        self,
        name: Optional[str] = None,
        duration: Optional[float] = None,
        priority: Optional[str] = None,
        frequency: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> None:
        """Update supplied fields; None leaves a field unchanged."""
        # Validate first so an invalid update does not partially change the task.
        if duration is not None and duration < 0:
            raise ValueError("Task duration cannot be negative.")
        if priority is not None and priority not in ("high", "medium", "low"):
            raise ValueError("Priority must be high, medium, or low.")

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

    def get_details(self) -> str:
        """Describe all task fields in a readable format."""
        status = "completed" if self.completed else "incomplete"
        return (
            f"{self.name}: {self.description} | "
            f"Duration: {self.duration} minutes | Priority: {self.priority} | "
            f"Frequency: {self.frequency} | Status: {status}"
        )

    def mark_completed(self) -> None:
        """Set the task's completion status to True."""
        self.completed = True

    def mark_complete(self) -> None:
        """Mark the task complete using the existing completion method."""
        self.mark_completed()

    def mark_incomplete(self) -> None:
        """Set the task's completion status to False."""
        self.completed = False


class Scheduler:
    """Access an owner's tasks; planning algorithms come in Phase 4."""

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
        """Phase 4 will define task sorting; no ordering algorithm exists yet."""
        raise NotImplementedError("Task sorting is reserved for Phase 4.")

    def detect_conflicts(self) -> bool:
        """Phase 4 will define scheduling conflicts and how to detect them."""
        raise NotImplementedError("Conflict detection is reserved for Phase 4.")

    def generate_schedule(self) -> List[Task]:
        """Phase 4 will build a plan using priorities, time, and recurrence."""
        raise NotImplementedError("Schedule generation is reserved for Phase 4.")
