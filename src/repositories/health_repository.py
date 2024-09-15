from sqlalchemy import select, func
from repositories.base import GenericRepository


class HealthCheckRepository(GenericRepository):
    async def get_db_time(self):
        query = select(func.now())
        result = await self._run_query(query)
        return result[0].scalar()
