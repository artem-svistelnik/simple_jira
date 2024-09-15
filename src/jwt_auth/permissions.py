from dependency_injector.wiring import Provide
from fastapi import Depends
from starlette.requests import Request

from containers.auth import AuthDI
from jwt_auth.auth_handler import decode_token
from models.user import RoleType
from services.auth_service import AuthService


def get_token(auth_header):
    if "Bearer" in auth_header:
        return auth_header.split(" ")[1]
    return auth_header


def has_task_permission(allowed_roles: list[RoleType]):
    service: AuthService = Provide[AuthDI.service].provider()

    async def wrapper(request: Request):
        service.set_service_db_session(request.state.db_session)
        payload = decode_token(get_token(request.headers["Authorization"]))
        user = await service.auth_repo.get_user_by_id(payload["user_id"])
        await service.check_allowed(user.role, allowed_roles)
        if pk := request.path_params.get("pk", None):
            await service.check_manager_or_assigned(user, int(pk))

    return Depends(wrapper)
