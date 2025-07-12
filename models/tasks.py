from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel


class TasksModel(BaseModel):
    """Model for task data."""

    name: str
    priority: Optional[str]
    deadline: Optional[str]
    status: Optional[str] = None
    task_id: Optional[str] = None


class Tasks(ABC):

    @abstractmethod
    def create_task(self, task_data: List[TasksModel]) -> bool:
        """Create a new task(s)"""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[TasksModel]:
        """Get a task by its ID"""
        pass

    @abstractmethod
    def update_task(self, task_id: str, task_data: TasksModel) -> bool:
        """Update an existing task"""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID"""
        pass

    @abstractmethod
    def list_tasks(self, priority: Optional[str] = None) -> List[TasksModel]:
        """List all tasks, optionally filtered by priority"""
        pass
