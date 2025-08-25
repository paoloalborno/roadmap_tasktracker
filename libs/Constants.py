from enum import Enum

JSON_REPO_PATH = "./repositories/data.json"

class TaskStatus(Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

    @classmethod
    def from_string(cls, status): #argomento cls è classe stess, non istanza
        try:
            return cls[status.lower()]
        except KeyError:
            return None

