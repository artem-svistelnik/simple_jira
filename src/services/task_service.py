from repositories.task_repository import TaskRepository
from schemas.task_schemas import TaskSchema
from schemas.task_schemas import UpdateTaskStatusSchema
from services.base import BaseService
import logging


class TaskService(BaseService):
    def __init__(self, task_repository: TaskRepository):
        self.task_repo = task_repository

    async def get_task(self, pk: int):
        return await self.task_repo.get_task(pk)

    async def get_tasks(self):
        return await self.task_repo.get_tasks()

    async def create_task(self, task_dta: TaskSchema):
        task = await self.task_repo.create_task(task_dta)
        return await self.get_task(task.id)

    async def update_task(self, pk, task_dta: TaskSchema):
        task = await self.task_repo.update_task(pk, task_dta)
        return await self.get_task(task.id)

    async def delete_task(self, pk):
        await self.task_repo.delete_where(self.task_repo.model.id == pk)

    async def update_task_status(self, pk, task_dta: UpdateTaskStatusSchema):
        await self.task_repo.update_where(
            self.task_repo.model.id == pk,
            status=task_dta.status,
        )
        return await self.get_task(pk)

    async def send_mail_mock(self, to_email: str, subject: str, body: str):
        print(f"Email sent to {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
