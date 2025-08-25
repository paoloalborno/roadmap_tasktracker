import logging

from services.CommandService import CommandService, return_command_list
from services.TaskCRUDChromaService import TaskCRUDChromaService
from services.TaskCRUDJSONService import TaskCRUDJSONService

#starting app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    command_service = None
    task_service = None
    print("Choose dataset between json and chroma")
    command_dataset = input()
    if command_dataset == 'json':
        task_service = TaskCRUDJSONService()
    elif command_dataset == 'chrome':
        task_service = TaskCRUDChromaService()
    else:
        print("Invalid dataset")
        exit()
    command_service = CommandService(task_service)
    print("Type commands to control task list - to quit type 'q'\n")
    print(f"Available commands: {return_command_list()}")

    while True:
        command = input(" > ")
        if command == "q":
            break
        else:
            print(command_service.route_command(command))

