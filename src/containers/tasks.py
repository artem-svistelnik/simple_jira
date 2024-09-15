from dependency_injector import containers, providers


from services.task_service import TaskService
from repositories.task_repository import TaskRepository


class TaskDI(containers.DeclarativeContainer):
    task_repository = providers.Factory(
        TaskRepository,
    )
    service = providers.Factory(
        TaskService,
        task_repository=task_repository,
    )
