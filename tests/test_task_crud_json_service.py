
from unittest.mock import MagicMock
from services.CommandService import CommandService
from services.TaskCRUDJSONService import TaskCRUDJSONService


#UNIT
def test_add_command():
    mock_service = MagicMock() #siccome CommandService ha come argomento un servizio che implementa interfaccia, lo simulo
    mock_service.add_task.return_value = 1
    command_service = CommandService(mock_service)
    output = command_service.route_command('add "test task"')
    mock_service.add_task.assert_called_once_with("test task")
    assert "Task added successfully (ID: 1)" in output

#INTEGRATION
def test_integration_add_command():
    task_service = TaskCRUDJSONService(repo_path="./tests/resources/test_data.json")
    command_service = CommandService(task_service)
    output = command_service.route_command('add "test task"')
    assert "Output: Task added successfully (ID: 1)" in output
