from pawpal_system import Pet, Task


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
