from dependency_injector import containers, providers


from services.health_service import HealthCheckService
from repositories.health_repository import HealthCheckRepository


class HeathDI(containers.DeclarativeContainer):
    health_repository = providers.Factory(
        HealthCheckRepository,
    )
    service = providers.Factory(
        HealthCheckService,
        health_repository=health_repository,
    )
