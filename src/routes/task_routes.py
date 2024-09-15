from dependency_injector.wiring import Provide

from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from containers.tasks import TaskDI
from jwt_auth.auth_bearer import JWTBearer
from jwt_auth.permissions import has_task_permission
from models import RoleType
from routes.depends import get_service
from schemas.task_schemas import TaskSchema
from schemas.task_schemas import ResponseTaskSchema
from schemas.task_schemas import UpdateTaskStatusSchema
from services.task_service import TaskService

task_router = APIRouter(prefix="/task", tags=["Task"])


@task_router.get(
    "/",
    dependencies=(
        Depends(JWTBearer()),
        has_task_permission([RoleType.ADMIN, RoleType.MANAGER, RoleType.USER]),
    ),
    response_model=list[ResponseTaskSchema],
)
async def get_tasks(service: TaskService = get_service(Provide[TaskDI.service])):
    tasks = await service.get_tasks()
    return [ResponseTaskSchema.from_orm(task) for task in tasks]


@task_router.get(
    "/{pk}",
    dependencies=(
        Depends(JWTBearer()),
        has_task_permission([RoleType.ADMIN, RoleType.MANAGER, RoleType.USER]),
    ),
    response_model=ResponseTaskSchema,
)
async def get_task(
    pk: int, service: TaskService = get_service(Provide[TaskDI.service])
):
    task = await service.get_task(pk)
    return ResponseTaskSchema.from_orm(task)


@task_router.post(
    "/",
    dependencies=(
        Depends(JWTBearer()),
        has_task_permission([RoleType.ADMIN, RoleType.MANAGER]),
    ),
    response_model=ResponseTaskSchema,
)
async def create_task(
    task_dta: TaskSchema, service: TaskService = get_service(Provide[TaskDI.service])
):
    task = await service.create_task(task_dta)
    return ResponseTaskSchema.from_orm(task)


@task_router.put(
    "/{pk}",
    dependencies=(
        Depends(JWTBearer()),
        has_task_permission([RoleType.ADMIN, RoleType.MANAGER]),
    ),
    response_model=ResponseTaskSchema,
)
async def update_task(
    pk: int,
    task_dta: TaskSchema,
    service: TaskService = get_service(Provide[TaskDI.service]),
):
    task = await service.update_task(pk, task_dta)
    return ResponseTaskSchema.from_orm(task)


@task_router.delete(
    "/{pk}",
    dependencies=(
        Depends(JWTBearer()),
        has_task_permission([RoleType.ADMIN, RoleType.MANAGER]),
    ),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    pk: int, service: TaskService = get_service(Provide[TaskDI.service])
):
    await service.delete_task(pk)


@task_router.put(
    "/change_status/{pk}",
    dependencies=(
        Depends(JWTBearer()),
        has_task_permission([RoleType.ADMIN, RoleType.MANAGER, RoleType.USER]),
    ),
    response_model=ResponseTaskSchema,
)
async def update_task_status(
    pk: int,
    task_dta: UpdateTaskStatusSchema,
    service: TaskService = get_service(Provide[TaskDI.service]),
):
    task = await service.update_task_status(pk, task_dta)

    subject = f"Task '{task.title}' status updated"
    body = f"The status of task '{task.title}' has been updated to {task.status}."
    await service.send_mail_mock(task.responsible_person_id, subject, body)

    return ResponseTaskSchema.from_orm(task)
