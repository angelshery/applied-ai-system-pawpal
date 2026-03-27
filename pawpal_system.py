from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    type: str        # e.g. "feeding", "walking", "medication"
    duration: int    # in minutes
    priority: int    # 1 = highest priority

    def get_details(self) -> str:
        return f"{self.name} ({self.type}) - {self.duration} min, priority {self.priority}"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time: int, preferences: List[str]):
        self.name = name
        self.available_time = available_time  # in minutes
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_available_time(self) -> int:
        return self.available_time


class Scheduler:
    def __init__(self):
        self.plan: List[Task] = []
        self.owner: Owner = None
        self.pet: Pet = None

    def generate_plan(self, owner: Owner, pet: Pet) -> List[Task]:
        self.owner = owner
        self.pet = pet
        # TODO: sort pet tasks by priority and fit within owner's available time
        pass

    def explain_plan(self) -> str:
        # uses self.owner and self.pet set during generate_plan
        pass
