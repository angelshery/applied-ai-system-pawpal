from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner with 60 minutes available
owner = Owner(name="Angel", available_time=60, preferences=["morning routine"])

# Create pets
dog = Pet(name="Biscuit", species="Dog", age=3, breed="Golden Retriever")
cat = Pet(name="Luna", species="Cat", age=2, breed="Siamese")

# Add tasks to Biscuit
dog.add_task(Task(name="Morning Walk", type="walking", duration=20, priority=1))
dog.add_task(Task(name="Breakfast", type="feeding", duration=10, priority=2))

# Add tasks to Luna
cat.add_task(Task(name="Medication", type="medication", duration=5, priority=1))
cat.add_task(Task(name="Playtime", type="enrichment", duration=15, priority=3))

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Generate and print the schedule
scheduler = Scheduler()
scheduler.generate_plan(owner)

print("=" * 40)
print("        Today's Schedule")
print("=" * 40)
print(scheduler.explain_plan())
print("=" * 40)
