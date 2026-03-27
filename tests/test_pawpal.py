from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", type="walking", duration=20, priority=1)
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Breakfast", type="feeding", duration=10, priority=2))
    assert len(pet.get_tasks()) == 1
