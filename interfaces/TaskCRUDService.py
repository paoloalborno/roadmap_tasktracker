from abc import ABC, abstractmethod
from typing import List
from models.Task import Task

class TaskCRUDService(ABC):
    def __init__(self, repo_type):
        self.repo_type = repo_type
        self.tasks: List[Task] = []
        pass

    def return_service_repo_type(self):
        return self.repo_type

    @abstractmethod
    def create_empty_repo(self):
        pass

    @abstractmethod
    def load_repo(self):
        pass

    @abstractmethod
    def add_task(self, task_description):
        pass

    @abstractmethod
    def list_tasks(self, task_status):
        pass

    @abstractmethod
    def delete_task(self, task_id):
        pass

    @abstractmethod
    def update_task(self, task_id, task_description, task_status):
        pass


