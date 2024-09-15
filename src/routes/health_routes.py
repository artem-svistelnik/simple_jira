from dependency_injector.wiring import Provide

from fastapi import APIRouter

from containers.health import HeathDI
from routes.depends import get_service
from services.health_service import HealthCheckService

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("")
async def health_check(
    service: HealthCheckService = get_service(Provide[HeathDI.service]),
):
    db_time = await service.get_db_time()
    return {"status": "ok", "database_time": db_time}
