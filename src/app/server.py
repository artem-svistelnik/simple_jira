import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import uvloop

from app.core.config import settings
from app.core.db_config import db_conf
from app.database import Database
from exceptions.base import ApiError, api_error_handler
from routes import include_routes


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with request.app.state.db.session() as db_session:
            request.state.db_session = db_session
            response = await call_next(request)
            if response.status_code <= 299:
                await request.state.db_session.commit()
        return response


def get_application():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        root_path=settings.ROOT_PATH,
    )
    _app.add_exception_handler(ApiError, api_error_handler)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # _app.add_middleware(JWTAuthenticationMiddleware)
    _app.add_middleware(DBSessionMiddleware)
    include_routes(_app)

    @_app.on_event("startup")
    async def open_database_connection_pools():
        db_connection = await Database(db_conf)  # noqa
        _app.state.db = db_connection

    @_app.on_event("shutdown")
    async def close_database_connection_pools():
        if _app.state.db:
            await _app.state.db.engine.dispose()

    return _app


app = get_application()
