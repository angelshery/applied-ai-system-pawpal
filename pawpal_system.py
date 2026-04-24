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
        self.guardrail_warnings: List[str] = []
        self.decision_log: List[str] = []

    def score_task(self, task: Task) -> float:
        """
        Calculate a score for a task based on priority, type, duration, and start time.
        Higher scores indicate higher priority for scheduling.
        
        Scoring factors:
        - Priority: Priority 1 gets the highest score (lower number = higher score)
        - Task type: Medication and feeding get extra weight
        - Duration: Shorter tasks get a small bonus
        - Start time: Earlier start times get a slight bonus
        """
        # Base score from priority (1 = highest priority, so we invert it)
        # Priority 1 -> 100 points, Priority 2 -> 90 points, etc.
        priority_score = (6 - task.priority) * 20
        
        # Extra weight for important task types
        type_bonus = 0
        if task.type.lower() == "medication":
            type_bonus = 30
        elif task.type.lower() == "feeding":
            type_bonus = 20
        
        # Bonus for shorter tasks (shorter = better chance to fit in schedule)
        # Max bonus of 10 points for tasks under 15 minutes
        duration_bonus = 0
        if task.duration < 15:
            duration_bonus = 10
        elif task.duration < 30:
            duration_bonus = 5
        
        # Small bonus for earlier start times
        # Parse "HH:MM" and convert to minutes from midnight
        hour, minute = map(int, task.start_time.split(":"))
        start_minutes = hour * 60 + minute
        # Earlier times get higher bonus (max 10 points for 6 AM, decreasing from there)
        time_bonus = max(0, 10 - (start_minutes - 360) // 60) if start_minutes >= 360 else 10
        
        # Total score
        total_score = priority_score + type_bonus + duration_bonus + time_bonus
        return total_score

    def validate_task(self, task: Task) -> bool:
        """
        Validate a task for scheduling.
        Returns True if valid, False otherwise.
        Checks for:
        - Missing task name
        - Duration <= 0
        - Priority outside 1-5
        - Invalid start_time format (must be HH:MM)
        """
        # Check for missing task name
        if not task.name or not task.name.strip():
            self.guardrail_warnings.append(f"Invalid task: missing name")
            return False
        
        # Check duration is positive
        if task.duration <= 0:
            self.guardrail_warnings.append(f"Invalid task '{task.name}': duration must be greater than 0")
            return False
        
        # Check priority is between 1 and 5
        if task.priority < 1 or task.priority > 5:
            self.guardrail_warnings.append(f"Invalid task '{task.name}': priority must be between 1 and 5")
            return False
        
        # Check start_time format (HH:MM)
        try:
            hour, minute = map(int, task.start_time.split(":"))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError()
        except (ValueError, AttributeError):
            self.guardrail_warnings.append(f"Invalid task '{task.name}': invalid start_time format (use HH:MM)")
            return False
        
        return True

    def generate_plan(self, owner: Owner) -> List[Task]:
        """Build a daily plan by sorting tasks by score and fitting them into available time."""
        self.owner = owner
        self.plan = []
        self.guardrail_warnings = []
        self.decision_log = []
        time_remaining = owner.get_available_time()

        # Sort all tasks by score (highest first), then fit into available time
        all_tasks = sorted(owner.get_all_tasks(), key=lambda t: self.score_task(t), reverse=True)

        for task in all_tasks:
            # Skip invalid tasks
            if not self.validate_task(task):
                continue
            if task.duration <= time_remaining:
                score = self.score_task(task)
                self.plan.append(task)
                self.decision_log.append(f"Scheduled '{task.name}' (score: {score})")
                time_remaining -= task.duration
            else:
                self.decision_log.append(f"Skipped '{task.name}' - not enough time")

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
        """Return a readable summary of the scheduled plan with explanations for each task."""
        if not self.plan:
            return "No tasks could be scheduled."

        lines = [f"Daily plan for {self.owner.name}:"]
        
        # Explain each task with its score and why it was selected
        for task in self.sort_by_time():
            score = self.score_task(task)
            lines.append(f"  - {task.name}")
            lines.append(f"    Type: {task.type}, Priority: {task.priority}, Duration: {task.duration} min, Start: {task.start_time}")
            lines.append(f"    Score: {score} (higher = more important)")
            lines.append("")

        total = sum(t.duration for t in self.plan)
        lines.append(f"Total time: {total} min of {self.owner.get_available_time()} min available.")
        return "\n".join(lines)
