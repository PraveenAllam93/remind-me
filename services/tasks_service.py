import hashlib
import time
import traceback
from typing import List, Optional

from config.settings import settings
from logs import get_app_logger, get_error_logger
from models.tasks import Tasks, TasksModel

from .redis_service import (
    delete_redis_hash,
    get_redis_hash_values,
    set_redis_hash_values,
)

app_logger = get_app_logger()
error_logger = get_error_logger()


class TasksService(Tasks):

    def __init__(self, userid: str = settings.DEFAULT_USER_ID):
        self.userid = userid
        # self.tasks = get_redis_hash_values(settings.REDIS_TASKS_KEY, userid)
        self.tasks = {}
        self.new_tasks = {}

    def create_task(self, task_data: List[TasksModel]) -> bool:
        old_tasks = get_redis_hash_values(f"{settings.REDIS_TASKS_KEY}-{self.userid}")
        if not old_tasks:
            old_tasks = {}

        for task in task_data:
            try:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                task_id = f"task_{hashlib.sha256(f"{task.get("name")}{current_time}{self.userid}".encode()).hexdigest()}"
                self.new_tasks[task_id] = task
                if task_id in old_tasks:
                    task["status"] = (
                        "Duplicate task ID found, updating the existing task."
                    )

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

        print(f"{self.new_tasks=}")
        set_redis_hash_values(
            f"{settings.REDIS_TASKS_KEY}-{self.userid}", self.new_tasks
        )

        return {"success": True, "task": task_data}

    def get_task(self, task_id: str) -> Optional[TasksModel]:
        return get_redis_hash_values(
            f"{settings.REDIS_TASKS_KEY}-{self.userid}", task_id
        )

    def update_task(self, task_id: str, task_data: TasksModel) -> bool:
        if task_id not in self.tasks:
            return False
        self.tasks[task_id] = task_data
        return True

    def delete_task(self, task_id: str) -> bool:
        is_deleted = delete_redis_hash(
            f"{settings.REDIS_TASKS_KEY}-{self.userid}", task_id
        )
        return is_deleted

    def list_tasks(self, priority: Optional[str] = None) -> List[TasksModel]:
        return get_redis_hash_values(f"{settings.REDIS_TASKS_KEY}-{self.userid}")
