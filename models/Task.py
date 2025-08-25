from datetime import datetime

from libs import Constants
from libs.Constants import TaskStatus


class Task:
    def __init__(self, task_description):
        self.task_id = None
        self.task_description = task_description
        self.task_status = Constants.TaskStatus.todo
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_time(self):
        self.updated_at = datetime.now()

    def set_status(self, task_status):
        self.task_status = task_status

    def set_id(self, task_id):
        self.task_id = task_id

    def set_description(self, task_description):
        self.task_description = task_description

    def get_id(self):
        return self.task_id

    def get_description(self):
        return self.task_description

    def get_status(self):
        return self.task_status

    def to_dict(self):
        return  {
                "task_id" : self.get_id(),
                "task_description" : self.get_description(),
                "task_status" : self.get_status().name,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
    def print_task(self):
        print(f" Task - ID : {self.get_id()} | Description : {self.get_description()} | Status : {self.get_status().name}")

    @classmethod #useful when creating an object from a dict - self does not exist yet
    def from_dict(cls, task_dict):
        task = Task(task_dict["task_description"])
        task.set_id(task_dict["task_id"])
        status = task_dict["task_status"]
        task.set_status(TaskStatus.from_string(status))
        if "created_at" in task_dict and task_dict["created_at"]:
            task.created_at = datetime.fromisoformat(task_dict["created_at"])
        if "updated_at" in task_dict and task_dict["updated_at"]:
            task.updated_at = datetime.fromisoformat(task_dict["updated_at"])

        return task

