from repositories.health_repository import HealthCheckRepository
from services.base import BaseService


class HealthCheckService(BaseService):
    def __init__(self, health_repository: HealthCheckRepository):
        self.health_repo = health_repository

    async def get_db_time(self):
        return await self.health_repo.get_db_time()
