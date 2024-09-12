import asyncio
import logging
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
    AsyncEngine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.db_config import DbConfig

logger = logging.getLogger(__name__)
Base = declarative_base()


class SingletonMeta(type):
    _instances = {}
    _lock: asyncio.Lock = asyncio.Lock()

    async def __call__(cls, *args, **kwargs):
        async with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    _session_factory = async_scoped_session(
        sessionmaker(
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        ),
        scopefunc=asyncio.current_task,
    )
    _engine: AsyncEngine = None
    _db_conf: DbConfig

    def __init__(self, db_conf: DbConfig) -> None:
        self._db_conf = db_conf
        self._engine = self.engine
        logger.info("DB driver:%s", self.engine.driver)

    @property
    def engine(self) -> AsyncEngine:
        if not self._engine:
            self._engine = create_async_engine(
                self._db_conf.DB_CONFIG,
                echo=self._db_conf.SQLALCHEMY_QUERY_DEBUG,
                future=True,
                isolation_level=self._db_conf.DB_ISOLATION_LEVEL,
                pool_size=self._db_conf.DB_POOL_SIZE,
                max_overflow=self._db_conf.DB_POOL_MAX_OVERFLOW,
                pool_use_lifo=True,
                pool_pre_ping=True,
                connect_args={"command_timeout": self._db_conf.DB_COMMAND_TIMEOUT},
            )
            self._session_factory.configure(bind=self._engine)
        return self._engine

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
            await self._session_factory.close()
            await self._session_factory.remove()

    def __del__(self):
        if self._engine:
            dispose_engine(self._engine)


def dispose_engine(engine):
    if engine:
        asyncio.run(engine.dispose())
