from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload

from models.user import User
from models.task import Task
from repositories.base import GenericRepository
from schemas.task_schemas import TaskSchema


class TaskRepository(GenericRepository[Task]):

    async def get_task(self, pk: int):
        query = (
            select(self.model)
            .where(self.model.id == pk)
            .options(
                joinedload(self.model.assignees),
            )
        )
        results = await self._run_query(query)
        return results[0].unique().scalars().first()

    async def get_tasks(self):
        query = select(self.model).options(
            joinedload(self.model.assignees),
        )
        results = await self._run_query(query)
        return results[0].unique().scalars().all()

    async def create_task(self, task_dta: TaskSchema):
        _task = self.model(
            **task_dta.dict(exclude={"assignees"}, exclude_defaults=True)
        )
        if task_dta.responsible_person_id:
            _task.responsible_person_id = task_dta.responsible_person_id
        if task_dta.assignees:
            assignees_query = select(User).where(User.id.in_(task_dta.assignees))
            assignees_result = await self._run_query(assignees_query)
            assignees = assignees_result[0].unique().scalars().all()
            _task.assignees.extend(assignees)

        return await self.create(_task, refresh=True)

    async def update_task(self, pk: int, task_dta: TaskSchema):
        _task = await self.get_task(pk)
        _task = task_dta.update_model(
            _task, exclude_fields=("assignees", "responsible_person_id")
        )
        if task_dta.responsible_person_id:
            _task.responsible_person_id = task_dta.responsible_person_id
        if task_dta.assignees:
            assignees_query = select(User).where(User.id.in_(task_dta.assignees))
            assignees_result = await self._run_query(assignees_query)
            new_assignees = assignees_result[0].unique().scalars().all()
            assignees_ids = [a.id for a in _task.assignees]
            if sorted(assignees_ids) != sorted(task_dta.assignees):
                _task.assignees = []
                _task.assignees.extend(new_assignees)

        return await self.update(_task, refresh=True)
