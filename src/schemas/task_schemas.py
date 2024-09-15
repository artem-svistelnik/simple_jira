from typing import Optional

from models import PriorityType
from models import StatusType
from schemas.base import BaseSchemaModel
from pydantic import Field

from schemas.user_schemas import UserSchema


class BaseTaskSchema(BaseSchemaModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=1000)
    status: StatusType
    priority: PriorityType


class ResponseTaskSchema(BaseTaskSchema):
    id: int
    responsible_person_id: Optional[int] = None
    assignees: Optional[list[UserSchema]] = None


class TaskSchema(BaseTaskSchema):
    responsible_person_id: Optional[int] = None
    assignees: Optional[list[int]] = None


class UpdateTaskStatusSchema(BaseSchemaModel):
    status: StatusType
