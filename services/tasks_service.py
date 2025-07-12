import hashlib
import time
import traceback
from typing import List, Optional

from logs import get_app_logger, get_error_logger
from models.tasks import Tasks, TasksModel

app_logger = get_app_logger()
error_logger = get_error_logger()


class TasksService(Tasks):

    def __init__(self, userid: str):
        self.userid = userid
        self.tasks = {}

    def create_task(self, task_data: List[TasksModel]) -> bool:
        for task in task_data:
            try:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                task_id = f"task_{hashlib.sha256(f"{task.get("name")}{current_time}{self.userid}".encode()).hexdigest()}"
                if task_id in self.tasks:
                    task["status"] = (
                        "Duplicate task ID found, updating the existing task."
                    )
                self.tasks[task_id] = task
                task["status"] = "Task created successfully, with ID: " + task_id
                app_logger.info(f"Task created: {task_id}")
            except Exception as e:
                error_logger.error(
                    f"Error creating task: {e}\n{task}\n{traceback.format_exc()}"
                )
                return {
                    "success": False,
                    "error": str(e),
                    "task": task,
                    "status": "Failed to create task",
                }
        return {"success": True, "task": task_data}

    def get_task(self, task_id: str) -> Optional[TasksModel]:
        return self.tasks.get(task_id)

    def update_task(self, task_id: str, task_data: TasksModel) -> bool:
        if task_id not in self.tasks:
            return False
        self.tasks[task_id] = task_data
        return True

    def delete_task(self, task_id: str) -> bool:
        if task_id not in self.tasks:
            return False
        del self.tasks[task_id]
        return True

    def list_tasks(self, priority: Optional[str] = None) -> List[TasksModel]:
        if priority is None or priority == "all":
            return list(self.tasks.values())
        return [
            task for task in self.tasks.values() if task.get("priority") == priority
        ]
