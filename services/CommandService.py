import logging
from interfaces.TaskCRUDService import TaskCRUDService
import re


def return_command_list():
    return "\n".join(["create repository", "reload repository", "add \"<task_name>\"", "delete <task_id>",
                     "update <task_id> \"<task_name>\"", "mark-<status> <task_id>", "list", "list <done, todo, in-progress>"])

class CommandService:
    def __init__(self, task_crud_service: TaskCRUDService): #ok passing interface
        self.task_crud_service = task_crud_service
        pass

    def route_command(self, command):
        create_repo_pattern = 'create repository'
        check_repo_pattern = 'reload repository'
        list_pattern = r'list(\s([\w-]+))?$'
        add_task_pattern = r'add\s"([^"]+)"$'
        delete_task_pattern = r'delete\s(\d+)'
        update_task_pattern = r'update\s(\d+)\s"([^"]+)"$'
        mark_task_pattern = r'mark-([\w-]+)\s(\d+)$'

        command_handlers = [
            (create_repo_pattern, self.handle_check_repo, False),
            (check_repo_pattern, self.handle_create_repo, False),
            (list_pattern, self.handle_list_tasks, True),
            (add_task_pattern, self.handle_add_task, True),
            (delete_task_pattern, self.handle_delete_task, True),
            (update_task_pattern, self.handle_update_task, True),
            (mark_task_pattern, self.handle_mark_task, True),
        ]

        for pattern, handler, is_regex in command_handlers:
            if is_regex:
                match = re.fullmatch(pattern, command)
                if match:
                    return handler(match)
            else:
                if command == pattern:
                    return handler(None)

        return "Command not recognized."

    def handle_check_repo(self, match=None):
        self.task_crud_service.load_repo()
        return "Output: Repository is valid!"

    def handle_create_repo(self, match=None):
        self.task_crud_service.create_empty_repo()
        return "Output: Empty Repository created!"

    def handle_list_tasks(self, match):
        status = match.groups()[1] if match else None
        self.task_crud_service.list_tasks(status)
        return "Output: Listed"

    def handle_add_task(self, match):
        task_description = match.groups()[0]
        task_id = self.task_crud_service.add_task(task_description)
        logging.info(f"Adding task to repository {self.task_crud_service.return_service_repo_type()}")
        return f"Output: Task added successfully (ID: {task_id})"

    def handle_delete_task(self, match):
        task_id = match.groups()[0]
        logging.info(f"Deleting task from repository {self.task_crud_service.return_service_repo_type()}")
        try:
            if self.task_crud_service.delete_task(task_id):
                return f"Output: Task deleted successfully (ID: {task_id})"
        except Exception as e:
            logging.error(f"Error deleting task with id {task_id} - {e}")
            return f"Error: {e}"

    def handle_update_task(self, match):
        task_id = match.groups()[0]
        task_description_update = match.groups()[1]
        logging.info(f"Updating task from repository {self.task_crud_service.return_service_repo_type()}")
        try:
            if self.task_crud_service.update_task(task_id, task_description=task_description_update, task_status=None):
                return f"Output: Task name updated successfully (ID: {task_id})"
        except Exception as e:
            logging.error(f"Error updating task with id {task_id} - {e}")
            return f"Error: {e}"

    def handle_mark_task(self, match):
        logging.info(f"Marking task from repository {self.task_crud_service.return_service_repo_type()}")
        task_status, task_id = match.groups()
        try:
            if self.task_crud_service.update_task(task_id, task_description=None, task_status=task_status):
                return f"Output: Task status updated successfully (ID: {task_id})"
        except Exception as e:
            logging.error(f"Error updating task with id {task_id} - {e}")
            return f"Error: {e}"




