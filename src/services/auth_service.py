from sqlalchemy import select
from sqlalchemy.orm import joinedload

from exceptions.auth_exceptions import PermissionDeniedError
from exceptions.base import NotFoundError
from models.user import RoleType
from models.task import Task
from repositories.user_repository import UserRepository
from services.base import BaseService


class AuthService(BaseService):
    def __init__(self, auth_repository: UserRepository):
        self.auth_repo = auth_repository

    async def check_allowed(self, user_role, allowed_roles: list[RoleType]):
        if user_role not in allowed_roles:
            raise PermissionDeniedError()

    async def get_task(self, pk):
        query = (
            select(Task)
            .where(Task.id == pk)
            .options(
                joinedload(Task.assignees),
            )
        )
        results = await self.auth_repo._run_query(query)
        return results[0].unique().scalars().first()

    async def get_task_manager(self, task):
        if task is not None:
            if task.responsible_person_id is not None:
                return task.responsible_person_id
            raise PermissionDeniedError()
        raise NotFoundError()

    async def get_task_assignee_ids(self, task):
        if task is not None:
            if task.assignees is not None:
                return [a.id for a in task.assignees]
            raise PermissionDeniedError()
        raise NotFoundError()

    async def check_manager_or_assigned(self, user, pk: int):
        match user.role:
            case RoleType.ADMIN:
                pass
            case RoleType.MANAGER:
                task = await self.get_task(pk)
                manager_id = await self.get_task_manager(task)
                if manager_id != user.id:
                    raise PermissionDeniedError()
            case RoleType.USER:
                task = await self.get_task(pk)
                assignee_ids = await self.get_task_assignee_ids(task)
                if user.id not in assignee_ids:
                    raise PermissionDeniedError()
