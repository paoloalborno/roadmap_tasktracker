from interfaces.TaskCRUDService import TaskCRUDService

class TaskCRUDChromaService(TaskCRUDService):

    def __init__(self):
        super().__init__("CHROMA")
        pass

    def create_empty_repo(self):
        pass

    def load_repo(self):
        pass

    def add_task(self, task_description):
        pass

    def delete_task(self, task_id):
        pass

    def update_task(self, task_id, task_description, task_status):
        pass

    def list_tasks(self, task_status):
        pass