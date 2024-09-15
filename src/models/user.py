import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Enum, Integer, String


class RoleType(str, enum.Enum):
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleType] = mapped_column(Enum(RoleType), default=RoleType.USER)

    manager_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    manager: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"user id {self.id}"
