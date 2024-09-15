from sqlalchemy import select

from jwt_auth.helpers import hash_password
from models.user import User
from repositories.base import GenericRepository
from schemas.user_schemas import SignUpSchema


class UserRepository(GenericRepository[User]):

    async def create_user(self, user: SignUpSchema):
        hashed_password = hash_password(user.password)
        user = await self.create(
            self.model(
                name=user.name,
                username=user.username,
                email=user.email,
                password=str(hashed_password),
            ),
            refresh=True,
        )
        return user

    async def get_user_by_username(self, username: str):
        query = select(self.model).where(self.model.username == username)
        results = await self._run_query(query)
        return results[0].unique().scalars().one()

    async def get_user_by_id(self, id: int):
        query = select(self.model).where(self.model.id == id)
        results = await self._run_query(query)
        return results[0].unique().scalars().one()
