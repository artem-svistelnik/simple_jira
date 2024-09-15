from exceptions.auth_exceptions import InvalidCredentials
from jwt_auth.helpers import verify_password
from repositories.user_repository import UserRepository
from schemas.user_schemas import LoginSchema
from schemas.user_schemas import SignUpSchema
from services.base import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def create_user(self, user: SignUpSchema):
        return await self.user_repo.create_user(user)

    async def authenticate_user(self, login_dta: LoginSchema):
        user = await self.user_repo.get_user_by_username(login_dta.username)

        if not verify_password(login_dta.password, user.password):
            raise InvalidCredentials()
        return user
