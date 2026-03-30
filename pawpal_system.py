from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    category: str
    duration: int
    priority: int
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass

    def reset(self) -> None:
        """Reset the task to incomplete."""
        pass

    def is_high_priority(self) -> bool:
        """Return True if the task is considered high priority."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str = ""
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        pass

    def set_preferences(self, preferences: Dict[str, str]) -> None:
        """Update owner preferences."""
        pass

    def view_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        pass


@dataclass
class Scheduler:
    owner: Owner
    daily_plan: List[Task] = field(default_factory=list)

    def collect_tasks(self) -> List[Task]:
        """Collect all available tasks from the owner's pets."""
        pass

    def generate_plan(self) -> List[Task]:
        """Generate a daily schedule based on time and priority."""
        pass

    def explain_plan(self) -> str:
        """Explain why the current daily plan was chosen."""
        pass

    def get_remaining_time(self) -> int:
        """Return the owner's remaining available time."""
        pass