"""Run a CLI preview of care tasks across an owner's pets."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="John", available_time=90)
    biscuit = Pet(name="Biscuit", breed="Golden Retriever", age=3)
    luna = Pet(name="Luna", breed="Persian Cat", age=2)
    owner.add_pet(biscuit)
    owner.add_pet(luna)

    biscuit.add_task(Task("Morning Walk", 30, "high", "daily"))
    biscuit.add_task(Task("Breakfast", 10, "high", "daily"))
    luna.add_task(Task("Feeding", 15, "high", "daily"))
    luna.add_task(Task("Grooming", 20, "medium", "daily"))

    scheduler = Scheduler(owner)
    all_tasks = scheduler.get_tasks()

    print("Today's Schedule - PawPal+")
    print(f"Owner: {owner.name}")
    print("Preliminary daily task preview (no automatic sorting or start times).")

    for pet in owner.pets:
        print(f"\n{pet.name} ({pet.breed})")
        # Display this pet's tasks from the combined owner-wide task list.
        for task in all_tasks:
            if task in pet.tasks:
                status = "completed" if task.completed else "incomplete"
                print(
                    f"- {task.name} | {task.duration} minutes | "
                    f"Priority: {task.priority} | Status: {status}"
                )


if __name__ == "__main__":
    main()
