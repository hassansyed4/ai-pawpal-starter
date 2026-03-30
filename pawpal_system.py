from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    """Represents a single care activity for a pet."""

    description: str
    time_minutes: int
    due_time: str
    frequency: str = "daily"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task complete and create the next recurring task if needed."""
        self.completed = True

        if self.frequency.lower() == "daily":
            return Task(
                description=self.description,
                time_minutes=self.time_minutes,
                due_time=self.due_time,
                frequency=self.frequency,
                completed=False,
                due_date=self.due_date + timedelta(days=1),
            )

        if self.frequency.lower() == "weekly":
            return Task(
                description=self.description,
                time_minutes=self.time_minutes,
                due_time=self.due_time,
                frequency=self.frequency,
                completed=False,
                due_date=self.due_date + timedelta(weeks=1),
            )

        return None

    def reset(self) -> None:
        """Reset the task to incomplete."""
        self.completed = False

    def is_completed(self) -> bool:
        """Return whether the task is completed."""
        return self.completed


@dataclass
class Pet:
    """Stores pet details and the tasks assigned to that pet."""

    name: str
    species: str
    age: int
    breed: str = ""
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_description: str) -> None:
        """Remove a task by description."""
        self.tasks = [task for task in self.tasks if task.description != task_description]

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages the owner profile and all pets."""

    name: str
    available_time_minutes: int
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's account."""
        self.pets.append(pet)

    def set_preferences(self, preferences: Dict[str, str]) -> None:
        """Update owner preferences."""
        self.preferences.update(preferences)

    def view_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """Retrieves, filters, sorts, and organizes tasks across the owner's pets."""

    owner: Owner
    daily_plan: List[dict] = field(default_factory=list)

    def collect_tasks(self) -> List[dict]:
        """Collect all tasks from the owner's pets."""
        collected_tasks: List[dict] = []
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                collected_tasks.append(
                    {
                        "pet_name": pet.name,
                        "species": pet.species,
                        "task": task,
                    }
                )
        return collected_tasks

    def sort_by_time(self, tasks: List[dict]) -> List[dict]:
        """Sort tasks by due time in HH:MM format."""
        return sorted(tasks, key=lambda item: item["task"].due_time)

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[dict]:
        """Filter tasks by completion status or pet name."""
        tasks = self.collect_tasks()

        if completed is not None:
            tasks = [item for item in tasks if item["task"].completed == completed]

        if pet_name:
            tasks = [item for item in tasks if item["pet_name"].lower() == pet_name.lower()]

        return tasks

    def generate_plan(self) -> List[dict]:
        """Generate a daily plan from incomplete tasks sorted by due time."""
        tasks = self.filter_tasks(completed=False)
        sorted_tasks = self.sort_by_time(tasks)

        self.daily_plan = []
        used_time = 0

        for item in sorted_tasks:
            task_time = item["task"].time_minutes
            if used_time + task_time <= self.owner.available_time_minutes:
                self.daily_plan.append(item)
                used_time += task_time

        return self.daily_plan

    def detect_conflicts(self, tasks: Optional[List[dict]] = None) -> List[str]:
        """Detect simple time conflicts where two tasks share the same due time."""
        if tasks is None:
            tasks = self.collect_tasks()

        warnings: List[str] = []
        seen_times: Dict[str, List[str]] = {}

        for item in tasks:
            due_time = item["task"].due_time
            label = f"{item['task'].description} for {item['pet_name']}"

            if due_time not in seen_times:
                seen_times[due_time] = [label]
            else:
                for existing in seen_times[due_time]:
                    warnings.append(
                        f"Conflict warning: '{existing}' and '{label}' are both scheduled at {due_time}."
                    )
                seen_times[due_time].append(label)

        return warnings

    def mark_task_complete(self, pet_name: str, task_description: str) -> bool:
        """Mark a task complete and create the next recurring instance when needed."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                for task in pet.tasks:
                    if task.description.lower() == task_description.lower() and not task.completed:
                        new_task = task.mark_complete()
                        if new_task is not None:
                            pet.add_task(new_task)
                        return True
        return False

    def explain_plan(self) -> str:
        """Explain how the current daily plan was created."""
        if not self.daily_plan:
            return "No tasks were scheduled for today."

        total_time = sum(item["task"].time_minutes for item in self.daily_plan)
        return (
            f"The plan includes {len(self.daily_plan)} task(s) within "
            f"{self.owner.available_time_minutes} available minutes. "
            f"Incomplete tasks were sorted by due time and added until the time limit was reached."
        )

    def get_remaining_time(self) -> int:
        """Return the remaining available time after scheduling."""
        used_time = sum(item["task"].time_minutes for item in self.daily_plan)
        return self.owner.available_time_minutes - used_time