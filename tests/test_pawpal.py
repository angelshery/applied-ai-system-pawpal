from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Helpers ---

def make_scheduler_with_tasks(*tasks):
    """Create an owner, add all tasks to one pet, and return a generated scheduler."""
    owner = Owner(name="Angel", available_time=120, preferences=[])
    pet = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    for task in tasks:
        pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    return scheduler


# --- Existing tests ---

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


# --- Sorting ---

def test_sort_by_time_returns_chronological_order():
    late  = Task(name="Grooming",  type="grooming", duration=10, priority=2, start_time="10:00")
    early = Task(name="Breakfast", type="feeding",  duration=10, priority=1, start_time="07:00")
    scheduler = make_scheduler_with_tasks(late, early)
    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks[0].start_time == "07:00"
    assert sorted_tasks[1].start_time == "10:00"


def test_sort_by_time_tiebreak_uses_priority():
    t1 = Task(name="Walk",     type="walking", duration=10, priority=2, start_time="08:00")
    t2 = Task(name="Medicine", type="medication", duration=10, priority=1, start_time="08:00")
    scheduler = make_scheduler_with_tasks(t1, t2)
    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks[0].name == "Medicine"  # priority 1 comes first


# --- Recurring tasks ---

def test_daily_task_returns_next_occurrence():
    today = date.today()
    task = Task(name="Walk", type="walking", duration=20, priority=1, frequency="daily", due_date=today)
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed == False


def test_once_task_returns_none():
    task = Task(name="Vet Visit", type="medication", duration=30, priority=1, frequency="once")
    next_task = task.mark_complete()
    assert next_task is None


# --- Conflict detection ---

def test_detect_conflicts_finds_duplicate_times():
    t1 = Task(name="Walk",     type="walking",  duration=20, priority=1, start_time="08:00")
    t2 = Task(name="Medicine", type="medication", duration=5, priority=2, start_time="08:00")
    scheduler = make_scheduler_with_tasks(t1, t2)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_no_warning_when_times_differ():
    t1 = Task(name="Walk",      type="walking", duration=20, priority=1, start_time="07:00")
    t2 = Task(name="Breakfast", type="feeding", duration=10, priority=2, start_time="08:00")
    scheduler = make_scheduler_with_tasks(t1, t2)
    assert scheduler.detect_conflicts() == []


# --- Filtering ---

def test_filter_by_completion_status():
    t1 = Task(name="Walk",      type="walking", duration=10, priority=1, start_time="07:00")
    t2 = Task(name="Breakfast", type="feeding", duration=10, priority=2, start_time="08:00")
    scheduler = make_scheduler_with_tasks(t1, t2)
    t1.mark_complete()
    assert len(scheduler.filter_tasks(completed=True))  == 1
    assert len(scheduler.filter_tasks(completed=False)) == 1


def test_filter_by_pet_name():
    owner = Owner(name="Angel", available_time=120, preferences=[])
    dog = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    cat = Pet(name="Luna",    species="Cat", age=2, breed="Siamese")
    dog.add_task(Task(name="Walk",       type="walking",    duration=20, priority=1, start_time="07:00"))
    cat.add_task(Task(name="Medication", type="medication", duration=5,  priority=2, start_time="08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    assert all(t.name == "Walk"       for t in scheduler.filter_tasks(pet_name="Biscuit"))
    assert all(t.name == "Medication" for t in scheduler.filter_tasks(pet_name="Luna"))


# --- Edge cases ---

def test_pet_with_no_tasks_does_not_crash():
    pet = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    assert pet.get_tasks() == []


def test_scheduler_with_no_tasks_returns_empty_plan():
    owner = Owner(name="Angel", available_time=60, preferences=[])
    pet = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    owner.add_pet(pet)
    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    assert scheduler.plan == []
    assert scheduler.detect_conflicts() == []


# --- AI Scheduling (score_task) ---

def test_medication_scores_higher_than_grooming():
    """Medication should score higher than grooming due to type bonus."""
    med_task = Task(name="Medicine", type="medication", duration=10, priority=2, start_time="08:00")
    groom_task = Task(name="Grooming", type="grooming", duration=10, priority=2, start_time="08:00")
    
    scheduler = Scheduler()
    med_score = scheduler.score_task(med_task)
    groom_score = scheduler.score_task(groom_task)
    
    assert med_score > groom_score, "Medication should score higher than grooming"


def test_invalid_priority_creates_guardrail_warning():
    """Invalid priority (outside 1-5) should create a warning and skip the task."""
    invalid_task = Task(name="Bad Task", type="walking", duration=20, priority=10, start_time="08:00")
    
    owner = Owner(name="Angel", available_time=120, preferences=[])
    pet = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    pet.add_task(invalid_task)
    owner.add_pet(pet)
    
    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    
    # Check that a warning was generated
    assert len(scheduler.guardrail_warnings) > 0
    assert any("priority" in w.lower() for w in scheduler.guardrail_warnings)
    # Check that the invalid task was not added to the plan
    assert invalid_task not in scheduler.plan


def test_explain_plan_includes_score():
    """explain_plan should include the task score or reasoning."""
    task = Task(name="Morning Walk", type="walking", duration=20, priority=1, start_time="07:00")
    
    owner = Owner(name="Angel", available_time=120, preferences=[])
    pet = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
    pet.add_task(task)
    owner.add_pet(pet)
    
    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    explanation = scheduler.explain_plan()
    
    # Check that the explanation includes score information
    assert "Score:" in explanation or "score" in explanation.lower()
