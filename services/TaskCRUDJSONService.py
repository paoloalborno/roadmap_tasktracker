import json
import os
import logging
from interfaces.TaskCRUDService import TaskCRUDService
from libs.Constants import JSON_REPO_PATH, TaskStatus
from models.Task import Task

class TaskCRUDJSONService(TaskCRUDService):

    def __init__(self, repo_path=None):
        super().__init__("JSON")
        self.repo_path = repo_path or JSON_REPO_PATH
        self.load_repo()

    def create_empty_repo(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(os.path.dirname(self.repo_path), exist_ok=True)
        with open(self.repo_path, "w") as json_file:
            json.dump([], json_file)

    def update_repo(self):
        with open(self.repo_path, "w") as json_file:
            json.dump([t.to_dict() for t in self.tasks], json_file, indent=4)

    def load_repo(self):
        try:
            with open(self.repo_path, "r") as json_file:
                data_json = json.load(json_file)
                if data_json and isinstance(data_json, list):
                    self.tasks = [Task.from_dict(t) for t in data_json]
                    logging.info(f"Repository loaded successfully, with {len(self.tasks)} tasks")
                    return True
        except FileNotFoundError:
            logging.warn(f"Repository not found, creating new repository at {self.repo_path}")
            self.create_empty_repo()
            return True
        except json.JSONDecodeError:
            logging.error(f"Repository is corrupted!")
            return False

    def list_tasks(self, task_status):
        if not self.tasks:
            print("No tasks found!")
            return
        task_status_enum = None
        if task_status is not None:
            task_status_enum = TaskStatus.from_string(task_status)
            if task_status_enum is None:
                logging.error(f"Invalid status '{task_status}' Available: {[s.name for s in TaskStatus]}")
                return

        for t in self.tasks:
            print(t.get_status())

        filtered = (
            self.tasks if task_status is None
            else [t for t in self.tasks if t.get_status().name == task_status_enum.name]
        )

        if not filtered:
            print(f"No {task_status or ''} tasks found!".strip())
        else:
            for task in filtered:
                task.print_task()

    def add_task(self, task_description):
        next_id = len(self.tasks) + 1
        t = Task(task_description)
        t.set_id(next_id)
        self.tasks.append(t)
        with open(self.repo_path, "w") as json_file:
            json.dump([t.to_dict() for t in self.tasks], json_file, indent=4)
        logging.info(f"Task {task_description} added with id {next_id}")
        return next_id

    def delete_task(self, task_id):
        try:
            task_to_delete = next(t for t in self.tasks if t.get_id() == int(task_id))
            if task_to_delete is not None:
                self.tasks.remove(task_to_delete)
                self.update_repo()
                return True
            else:
                logging.error(f"Task with id {task_id} not found!")
                return False
        except Exception as e:
            logging.error(f"Error: {e}")
            return False

    def update_task(self, task_id, task_description, task_status):
        try:
            task_to_update = next((t for t in self.tasks if t.get_id() == int(task_id)), None)
            if task_to_update is None:
                logging.error(f"Task with id {task_id} not found")
                return False

            if task_status is not None:
                task_status_enum = TaskStatus.from_string(task_status)
                if task_status_enum is None:
                    logging.error(f"Invalid status '{task_status}' Available: {[s.name for s in TaskStatus]}")
                    return False
                task_to_update.set_status(task_status_enum)

            if task_description is not None:
                task_to_update.set_description(task_description)

            task_to_update.update_time()
            self.update_repo()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            return False