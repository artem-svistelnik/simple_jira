from dependency_injector import containers, providers


from services.user_service import UserService
from repositories.user_repository import UserRepository


class UserDI(containers.DeclarativeContainer):
    user_repository = providers.Factory(
        UserRepository,
    )
    service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
