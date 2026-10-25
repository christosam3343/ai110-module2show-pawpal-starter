"""Run a CLI preview of care tasks across an owner's pets."""

from datetime import date
from typing import List

from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(owner: Owner, tasks: List[Task]) -> None:
    """Print each task with its pet name and recorded care details."""
    for task in tasks:
        for pet in owner.pets:
            if any(pet_task is task for pet_task in pet.tasks):
                status = "completed" if task.completed else "incomplete"
                due_date = task.due_date.isoformat() if task.due_date is not None else "not set"
                print(
                    f"- {task.time or 'Untimed'} | {pet.name} | {task.name} | "
                    f"{task.duration} minutes | Priority: {task.priority} | Due: {due_date} | Status: {status}"
                )


def main() -> None:
    owner = Owner(name="John", available_time=90)
    biscuit = Pet(name="Biscuit", breed="Golden Retriever", age=3)
    luna = Pet(name="Luna", breed="Persian Cat", age=2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)
    # A fixed date makes the demonstration repeatable.
    completion_date = date(2026, 10, 24)

    # Enter times out of chronological order to demonstrate sorting.
    biscuit.add_task(Task("Morning Walk", 30, "high", "daily", time="09:00", due_date=completion_date))
    breakfast = Task("Breakfast", 10, "high", "daily", time="08:00", due_date=completion_date)
    biscuit.add_task(breakfast)
    luna.add_task(Task("Feeding", 15, "high", "daily", time="07:30", due_date=completion_date))
    grooming = Task("Grooming", 20, "medium", "weekly", time="10:00", due_date=completion_date)
    luna.add_task(grooming)
    # This overlaps Biscuit's 09:00-09:30 walk on the same date.
    luna.add_task(Task("Playtime", 20, "low", "once", time="09:15", due_date=completion_date))

    scheduler = Scheduler(owner)
    all_tasks = scheduler.get_tasks()

    print("Today's Schedule - PawPal+")
    print(f"Owner: {owner.name}")
    print("Times are entered manually; overlap warnings do not move tasks.")

    for pet in owner.pets:
        print(f"\n{pet.name} ({pet.breed})")
        pet_tasks = [task for task in all_tasks if any(task is pet_task for pet_task in pet.tasks)]
        print_tasks(owner, pet_tasks)

    print("\nAll pets - sorted by time")
    print_tasks(owner, scheduler.sort_by_time())

    print("\nBiscuit - incomplete tasks")
    print_tasks(owner, scheduler.filter_tasks(pet_name="Biscuit", completed=False))

    print(f"\nRecurring task completion demo - completed on {completion_date.isoformat()}")
    for pet, task in [(biscuit, breakfast), (luna, grooming)]:
        next_task = pet.complete_task(task, completion_date=completion_date)
        print(f"\n{pet.name} - {task.frequency}: completed original (kept in pet's task list)")
        print_tasks(owner, [task])
        if next_task is not None:
            print("New incomplete occurrence:")
            print_tasks(owner, [next_task])

    print("\nConflict check - incomplete tasks with a due date and clock time")
    print("Tasks missing a due date or clock time are unscheduled and were not checked.")
    warnings = scheduler.detect_conflicts()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No overlaps found among the scheduled incomplete tasks checked.")


if __name__ == "__main__":
    main()
