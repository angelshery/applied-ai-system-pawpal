from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    type: str            # e.g. "feeding", "walking", "medication"
    duration: int        # in minutes
    priority: int        # 1 = highest priority
    completed: bool = False

    def get_details(self) -> str:
        """Return a formatted string with the task's name, type, duration, and priority."""
        return f"{self.name} ({self.type}) - {self.duration} min, priority {self.priority}"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


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

    def explain_plan(self) -> str:
        """Return a readable summary of the scheduled plan and total time used."""
        if not self.plan:
            return "No tasks could be scheduled."

        lines = [f"Daily plan for {self.owner.name}:"]
        for task in self.plan:
            lines.append(f"  - {task.get_details()}")

        total = sum(t.duration for t in self.plan)
        lines.append(f"Total time: {total} min of {self.owner.get_available_time()} min available.")
        return "\n".join(lines)
