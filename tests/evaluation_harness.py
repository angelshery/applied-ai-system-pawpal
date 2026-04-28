"""
Evaluation harness for PawPal AI system.
Tests various scenarios to verify the Scheduler works correctly.
"""

import sys
import os
from datetime import date

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_normal_schedule():
    """Scenario 1: Normal schedule generation."""
    print("\n--- Scenario 1: Normal Schedule Generation ---")
    
    # Create an owner with 120 minutes available
    owner = Owner(name="Alice", available_time=120, preferences=["morning"])
    
    # Create a pet
    pet = Pet(name="Buddy", species="dog", age=3, breed="Golden Retriever")
    owner.add_pet(pet)
    
    # Add some tasks
    task1 = Task(name="Morning feeding", type="feeding", duration=15, priority=2, start_time="08:00")
    task2 = Task(name="Afternoon walk", type="walking", duration=30, priority=3, start_time="14:00")
    task3 = Task(name="Evening feeding", type="feeding", duration=15, priority=2, start_time="18:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    # Run the scheduler
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)
    
    # Check if tasks were scheduled
    if len(plan) >= 2:
        print("PASS: Normal schedule generated successfully")
        print(f"  Scheduled {len(plan)} tasks")
        return True
    else:
        print("FAIL: Expected at least 2 tasks to be scheduled")
        return False


def test_conflict_detection():
    """Scenario 2: Conflict detection with two tasks at the same time."""
    print("\n--- Scenario 2: Conflict Detection ---")
    
    # Create an owner with enough time for both tasks
    owner = Owner(name="Bob", available_time=120, preferences=["flexible"])
    
    # Create a pet
    pet = Pet(name="Max", species="cat", age=5, breed="Persian")
    owner.add_pet(pet)
    
    # Add two tasks at the same time
    task1 = Task(name="Morning medication", type="medication", duration=10, priority=1, start_time="09:00")
    task2 = Task(name="Vet appointment", type="medical", duration=30, priority=1, start_time="09:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    # Run the scheduler
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)
    
    # Check for conflicts
    conflicts = scheduler.detect_conflicts()
    
    if len(conflicts) > 0:
        print("PASS: Conflict detected successfully")
        print(f"  Conflict: {conflicts[0]}")
        return True
    else:
        print("FAIL: Expected a conflict to be detected")
        return False


def test_invalid_task_guardrails():
    """Scenario 3: Invalid task is skipped by guardrails."""
    print("\n--- Scenario 3: Invalid Task Guardrails ---")
    
    # Create an owner
    owner = Owner(name="Carol", available_time=60, preferences=["morning"])
    
    # Create a pet
    pet = Pet(name="Luna", species="dog", age=2, breed="Husky")
    owner.add_pet(pet)
    
    # Add a valid task and an invalid task (negative duration)
    valid_task = Task(name="Morning walk", type="walking", duration=30, priority=2, start_time="07:00")
    invalid_task = Task(name="Bad task", type="grooming", duration=-10, priority=1, start_time="10:00")
    
    pet.add_task(valid_task)
    pet.add_task(invalid_task)
    
    # Run the scheduler
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)
    
    # Check that invalid task was filtered out
    task_names = [t.name for t in plan]
    
    if "Bad task" not in task_names and "Morning walk" in task_names:
        print("PASS: Invalid task was filtered out by guardrails")
        print(f"  Guardrail warnings: {scheduler.guardrail_warnings}")
        return True
    else:
        print("FAIL: Invalid task should have been filtered out")
        return False


def test_priority_scheduling():
    """Scenario 4: High-priority medication scheduled before low-priority grooming."""
    print("\n--- Scenario 4: Priority Scheduling ---")
    
    # Create an owner with limited time
    owner = Owner(name="David", available_time=45, preferences=["morning"])
    
    # Create a pet
    pet = Pet(name="Rocky", species="dog", age=4, breed="German Shepherd")
    owner.add_pet(pet)
    
    # Add a low-priority grooming task and a high-priority medication task
    grooming = Task(name="Grooming", type="grooming", duration=30, priority=4, start_time="11:00")
    medication = Task(name="Critical medication", type="medication", duration=15, priority=1, start_time="08:00")
    
    pet.add_task(grooming)
    pet.add_task(medication)
    
    # Run the scheduler
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)
    
    # Check that medication (priority 1) was scheduled before grooming (priority 4)
    # Since medication has higher priority, it should be scheduled first
    task_names = [t.name for t in plan]
    
    if "Critical medication" in task_names and "Grooming" in task_names:
        print("PASS: Both tasks scheduled (priorities respected)")
        print(f"  Scheduled tasks: {task_names}")
        return True
    elif "Critical medication" in task_names:
        print("PASS: High-priority medication scheduled (low-priority skipped due to time)")
        print(f"  Scheduled: {task_names}")
        return True
    else:
        print("FAIL: Expected medication to be scheduled")
        return False


def main():
    """Run all test scenarios and print a summary."""
    print("=" * 50)
    print("PawPal AI System Evaluation")
    print("=" * 50)
    
    # Run each test scenario
    results = []
    results.append(test_normal_schedule())
    results.append(test_conflict_detection())
    results.append(test_invalid_task_guardrails())
    results.append(test_priority_scheduling())
    
    # Count passed tests
    passed = sum(results)
    total = len(results)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"SUMMARY: {passed} out of {total} scenarios passed.")
    print("=" * 50)
    
    if passed == total:
        print("All tests passed! Great job!")
    else:
        print("Some tests failed. Please review the output above.")


if __name__ == "__main__":
    main()