from dependency_injector import containers, providers


from services.auth_service import AuthService
from repositories.user_repository import UserRepository


class AuthDI(containers.DeclarativeContainer):
    auth_repository = providers.Factory(
        UserRepository,
    )
    service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
    )
