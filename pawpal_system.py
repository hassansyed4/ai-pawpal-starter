from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Task:
    """Represents a single care activity for a pet."""

    description: str
    time_minutes: int
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

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
    """Retrieves and organizes tasks across the owner's pets."""

    owner: Owner
    daily_plan: List[dict] = field(default_factory=list)

    def collect_tasks(self) -> List[dict]:
        """Collect all incomplete tasks from the owner's pets."""
        collected_tasks: List[dict] = []
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if not task.completed:
                    collected_tasks.append(
                        {
                            "pet_name": pet.name,
                            "species": pet.species,
                            "task": task,
                        }
                    )
        return collected_tasks

    def generate_plan(self) -> List[dict]:
        """Generate a daily plan within the owner's available time."""
        collected_tasks = self.collect_tasks()
        collected_tasks.sort(key=lambda item: item["task"].time_minutes)

        self.daily_plan = []
        used_time = 0

        for item in collected_tasks:
            task_time = item["task"].time_minutes
            if used_time + task_time <= self.owner.available_time_minutes:
                self.daily_plan.append(item)
                used_time += task_time

        return self.daily_plan

    def explain_plan(self) -> str:
        """Explain how the current daily plan was created."""
        if not self.daily_plan:
            return "No tasks were scheduled for today."

        total_time = sum(item["task"].time_minutes for item in self.daily_plan)
        return (
            f"The schedule includes {len(self.daily_plan)} task(s) "
            f"that fit within {self.owner.available_time_minutes} available minutes. "
            f"Tasks were selected from all pets and ordered by shortest duration first."
        )

    def get_remaining_time(self) -> int:
        """Return the remaining available time after scheduling."""
        used_time = sum(item["task"].time_minutes for item in self.daily_plan)
        return self.owner.available_time_minutes - used_time