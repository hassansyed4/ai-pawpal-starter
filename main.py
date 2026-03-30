from pawpal_system import Owner, Pet, Task, Scheduler


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


def test_sort_by_time_orders_tasks_correctly():
    owner = Owner(name="Test", available_time_minutes=60)
    pet = Pet(name="Buddy", species="Dog", age=4)

    pet.add_task(Task(description="Late Task", time_minutes=10, due_time="10:00"))
    pet.add_task(Task(description="Early Task", time_minutes=10, due_time="08:00"))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(scheduler.collect_tasks())

    assert sorted_tasks[0]["task"].description == "Early Task"
    assert sorted_tasks[1]["task"].description == "Late Task"


def test_filter_tasks_by_pet_name():
    owner = Owner(name="Test", available_time_minutes=60)
    dog = Pet(name="Buddy", species="Dog", age=4)
    cat = Pet(name="Milo", species="Cat", age=2)

    dog.add_task(Task(description="Walk", time_minutes=20, due_time="08:00"))
    cat.add_task(Task(description="Brush", time_minutes=15, due_time="09:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    results = scheduler.filter_tasks(pet_name="Buddy")

    assert len(results) == 1
    assert results[0]["pet_name"] == "Buddy"


def test_detect_conflicts_returns_warning():
    owner = Owner(name="Test", available_time_minutes=60)
    dog = Pet(name="Buddy", species="Dog", age=4)
    cat = Pet(name="Milo", species="Cat", age=2)

    dog.add_task(Task(description="Walk", time_minutes=20, due_time="09:00"))
    cat.add_task(Task(description="Brush", time_minutes=15, due_time="09:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) >= 1