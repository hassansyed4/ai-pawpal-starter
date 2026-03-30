from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    task = Task(description="Feed dinner", time_minutes=10, due_time="18:00")
    assert task.completed is False

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=4)
    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Walk", time_minutes=20, due_time="08:00"))

    assert len(pet.tasks) == 1