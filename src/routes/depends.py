from fastapi import Depends
from starlette.requests import Request


def get_service(provider):
    def _get_service(request: Request):
        service = provider.provider()
        service.set_service_db_session(request.state.db_session)
        return service

    return Depends(_get_service)
