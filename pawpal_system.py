from dataclasses import dataclass, field
from typing import Dict, List, Optional


class Owner:
    def __init__(
        self,
        name: str,
        available_time: float,
        preferences: Optional[Dict[str, object]] = None,
    ) -> None:
        self.name = name
        self.available_time = available_time
        self.preferences = preferences if preferences is not None else {}

    def add_pet(self, pet: "Pet") -> None:
        pass

    def update_availability(self, time: float) -> None:
        pass


@dataclass
class Pet:
    name: str
    breed: str
    age: int
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        pass

    def remove_task(self, task: "Task") -> None:
        pass


@dataclass
class Task:
    name: str
    duration: float
    priority: str
    frequency: str

    def update_task(self) -> None:
        pass

    def get_details(self) -> str:
        pass


class Scheduler:
    def __init__(
        self,
        tasks: Optional[List[Task]] = None,
        available_time: float = 0.0,
    ) -> None:
        self.tasks = tasks if tasks is not None else []
        self.available_time = available_time

    def sort_tasks(self) -> List[Task]:
        pass

    def detect_conflicts(self) -> bool:
        pass

    def generate_schedule(self) -> List[Task]:
        pass
