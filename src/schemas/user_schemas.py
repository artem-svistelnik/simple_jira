from schemas.base import BaseSchemaModel
from pydantic import EmailStr, Field


class SignUpSchema(BaseSchemaModel):
    name: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=8, max_length=100)
    email: EmailStr | None = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)


class LoginSchema(BaseSchemaModel):
    username: str = Field(min_length=8, max_length=255)
    password: str = Field(min_length=8, max_length=255)


class UserSchema(BaseSchemaModel):
    id: int
    name: str
    username: str
