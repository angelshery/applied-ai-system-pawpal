from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner with 60 minutes available
owner = Owner(name="Angel", available_time=60, preferences=["morning routine"])

# Create pets
dog = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
cat = Pet(name="Luna", species="Cat", age=2, breed="Siamese")

# Add tasks out of order to demonstrate sorting
dog.add_task(Task(name="Morning Walk", type="walking", duration=20, priority=1, start_time="08:00", frequency="daily"))
dog.add_task(Task(name="Breakfast",    type="feeding",  duration=10, priority=2, start_time="07:00", frequency="daily"))

cat.add_task(Task(name="Medication",   type="medication",  duration=5,  priority=1, start_time="09:00", frequency="daily"))
cat.add_task(Task(name="Playtime",     type="enrichment",  duration=15, priority=3, start_time="08:00", frequency="once"))

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Generate plan
scheduler = Scheduler()
scheduler.generate_plan(owner)

# --- Tasks as added (unsorted) ---
print("=" * 40)
print("   Tasks Added (original order)")
print("=" * 40)
for task in scheduler.plan:
    print(f"  {task.start_time} - {task.name}")

# --- Sorted by start time ---
print("\n" + "=" * 40)
print("   Sorted Schedule (by start time)")
print("=" * 40)
for task in scheduler.sort_by_time():
    print(f"  {task.start_time} - {task.name}")

# --- Full plan summary ---
print("\n" + "=" * 40)
print("        Today's Schedule")
print("=" * 40)
print(scheduler.explain_plan())
print("=" * 40)

# --- Conflict Detection ---
# Morning Walk (08:00) and Playtime (08:00) intentionally share the same start time
print("\n--- Conflict Detection ---")
print("  Checking for tasks scheduled at the same time...")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

# --- Filtering demos ---

# Mark one task complete so the filters show a difference
dog.get_tasks()[1].mark_complete()  # Breakfast marked complete

print("\n--- All Incomplete Tasks ---")
incomplete = scheduler.filter_tasks(completed=False)
for t in incomplete:
    print(f"  - {t.get_details()}")

print("\n--- All Completed Tasks ---")
completed = scheduler.filter_tasks(completed=True)
for t in completed:
    print(f"  - {t.get_details()}")

print("\n--- Biscuit's Tasks ---")
biscuit_tasks = scheduler.filter_tasks(pet_name="Biscuit")
for t in biscuit_tasks:
    print(f"  - {t.get_details()}")

print("\n--- Luna's Tasks ---")
luna_tasks = scheduler.filter_tasks(pet_name="Luna")
for t in luna_tasks:
    print(f"  - {t.get_details()}")

# --- Recurring Tasks ---
print("\n--- Recurring Task Demo ---")
task = dog.get_tasks()[0]  # Morning Walk (frequency="daily")
print(f"Before: {task.name} | due {task.due_date} | completed: {task.completed}")

next_task = task.mark_complete()
print(f"After:  {task.name} | due {task.due_date} | completed: {task.completed}")

if next_task:
    dog.add_task(next_task)
    print(f"Next:   {next_task.name} | due {next_task.due_date} | completed: {next_task.completed}")
