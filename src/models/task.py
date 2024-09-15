import enum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Enum, Integer, String
from models.user import User


class StatusType(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class PriorityType(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


task_assignees = Table(
    "task_assignees",
    Base.metadata,
    Column(
        "task_id", Integer, ForeignKey("task.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    status: Mapped[StatusType] = mapped_column(
        Enum(StatusType), default=StatusType.TODO
    )
    priority: Mapped[PriorityType] = mapped_column(
        Enum(PriorityType), default=PriorityType.HIGH
    )

    responsible_person_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    responsible_person: Mapped["User"] = relationship("User")

    assignees = relationship(
        "User", secondary=task_assignees, back_populates="tasks_assigned"
    )

    def __repr__(self):
        return f"task id: {self.id}"


User.tasks_assigned = relationship(
    "Task", secondary=task_assignees, back_populates="assignees"
)
