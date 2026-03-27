from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    name: str
    type: str            # e.g. "feeding", "walking", "medication"
    duration: int        # in minutes
    priority: int        # 1 = highest priority
    start_time: str = "08:00"   # "HH:MM" format
    frequency: str = "once"     # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def get_details(self) -> str:
        """Return a formatted string with the task's name, type, duration, and priority."""
        return f"{self.name} ({self.type}) - {self.duration} min, priority {self.priority}, starts {self.start_time}"

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next recurrence if frequency is daily or weekly."""
        self.completed = True
        if self.frequency == "daily":
            return Task(
                name=self.name,
                type=self.type,
                duration=self.duration,
                priority=self.priority,
                start_time=self.start_time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                name=self.name,
                type=self.type,
                duration=self.duration,
                priority=self.priority,
                start_time=self.start_time,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return the list of tasks assigned to this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time: int, preferences: List[str]):
        self.name = name
        self.available_time = available_time  # in minutes
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        return self.available_time

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self):
        self.plan: List[Task] = []
        self.owner: Owner = None

    def generate_plan(self, owner: Owner) -> List[Task]:
        """Build a daily plan by sorting tasks by priority and fitting them into available time."""
        self.owner = owner
        self.plan = []
        time_remaining = owner.get_available_time()

        # Sort all tasks by priority (1 = highest), then fit into available time
        all_tasks = sorted(owner.get_all_tasks(), key=lambda t: t.priority)

        for task in all_tasks:
            if task.duration <= time_remaining:
                self.plan.append(task)
                time_remaining -= task.duration

        return self.plan

    def sort_by_time(self) -> List[Task]:
        """Return the current plan sorted by start_time in HH:MM format."""
        return sorted(self.plan, key=lambda t: (t.start_time, t.priority))

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> List[Task]:
        """Return scheduled tasks filtered by pet name, completion status, or both."""
        # Build a lookup so we can check which pet owns each task
        task_to_pet = {}
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                task_to_pet[id(task)] = pet.name

        results = self.plan
        if pet_name is not None:
            results = [t for t in results if task_to_pet.get(id(t)) == pet_name]
        if completed is not None:
            results = [t for t in results if t.completed == completed]
        return results

    def detect_conflicts(self) -> List[str]:
        """Return a list of warning messages for tasks that share the same start time."""
        seen = {}
        warnings = []
        for task in self.plan:
            if task.start_time in seen:
                warnings.append(
                    f"Conflict at {task.start_time}: '{seen[task.start_time]}' and '{task.name}' overlap."
                )
            else:
                seen[task.start_time] = task.name
        return warnings

    def explain_plan(self) -> str:
        """Return a readable summary of the scheduled plan and total time used."""
        if not self.plan:
            return "No tasks could be scheduled."

        lines = [f"Daily plan for {self.owner.name}:"]
        for task in self.sort_by_time():
            lines.append(f"  - {task.get_details()}")

        total = sum(t.duration for t in self.plan)
        lines.append(f"Total time: {total} min of {self.owner.get_available_time()} min available.")
        return "\n".join(lines)
