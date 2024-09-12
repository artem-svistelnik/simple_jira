import asyncio
from typing import Generic, Type, TypeVar, get_args

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import Base
from exceptions.base import DataConflictError, MultipleResultsError, NotFoundError

ModelT = TypeVar("ModelT", bound=Base)


class GenericRepository(Generic[ModelT]):
    model: Type[ModelT]
    primary_key: str = "id"
    _s: AsyncSession

    def __init__(self):
        self.model = get_args(self.__orig_bases__[0])[0]  # type: ignore

    def set_session(self, session):
        self._s = session

    async def _run_query(self, *queries, commit=False) -> list:
        tasks = []
        for query in queries:
            tasks.append(asyncio.create_task(self._s.execute(query)))
        response = await asyncio.gather(*tasks)
        if commit:
            await self._s.flush()
        return response  # type: ignore

    def _count_query(self, *filters):
        return select(func.count(getattr(self.model, self.primary_key))).where(*filters)

    @staticmethod
    def _get_results(data, joined=False):
        if joined:
            return data.scalars().unique().all()
        return data.scalars().all()

    async def get(self, pk) -> ModelT:
        results = await self._run_query(
            select(self.model).where(getattr(self.model, self.primary_key) == pk)
        )
        try:
            return results[0].unique().scalars().one()
        except NoResultFound as e:
            raise NotFoundError() from e
        except MultipleResultsFound as e:
            raise MultipleResultsError() from e

    async def all(
        self,
        limit: int = None,
        offset: int = None,
        count: bool = False,
        order_by: list = None,
        join_load: dict[object, list[str] | str] = None,
    ) -> tuple[list[ModelT], int | None]:
        query = select(self.model).limit(limit).offset(offset)
        if join_load:
            query = query.options(
                *[
                    (
                        joinedload(table)
                        if fields == "*"
                        else joinedload(table).load_only(*fields)
                    )
                    for table, fields in join_load.items()
                ]
            )
        if order_by:
            query = query.order_by(*order_by)
        queries = [query]
        if count:
            queries.append(self._count_query())
        result = await self._run_query(*queries)
        match result:
            case data, _count:
                return (
                    self._get_results(data, joined=bool(join_load)),
                    _count.scalars().one(),
                )
            case data,:
                return self._get_results(data, joined=bool(join_load)), None

    async def filter(
        self,
        *filters,
        limit: int = None,
        offset: int = None,
        order_by: list = None,
        count: bool = False,
        join_load: dict[object, list[str] | str] = None,
    ) -> tuple[list[ModelT], int | None]:
        query = select(self.model).where(*filters).limit(limit).offset(offset)
        if join_load:
            query = query.options(
                *[
                    (
                        joinedload(table)
                        if fields == "*"
                        else joinedload(table).load_only(*fields)
                    )
                    for table, fields in join_load.items()
                ]
            )
        if order_by:
            query = query.order_by(*order_by)
        queries = [query]
        if count:
            queries.append(self._count_query(*filters))
        results = await self._run_query(*queries)
        match results:
            case data, _count:
                return (
                    self._get_results(data, joined=bool(join_load)),
                    _count.scalars().one(),
                )
            case data,:
                return self._get_results(data, joined=bool(join_load)), None

    async def create(self, model: ModelT, refresh=False) -> ModelT | None:
        try:
            self._s.add(model)
            await self._s.flush()
        except IntegrityError as e:
            raise DataConflictError() from e
        if refresh:
            await self._s.refresh(model)
            return model

    async def create_many(self, models: list[ModelT]):
        try:
            self._s.add_all(models)
        except IntegrityError as e:
            raise DataConflictError() from e

    async def update_where(self, *filters, **fields) -> int:
        cnt = await self._run_query(update(self.model).where(*filters).values(**fields))
        self._s.expire_all()
        return cnt[0]

    async def update(self, model: ModelT, refresh=False) -> ModelT | None:
        try:
            self._s.add(model)
            await self._s.flush()
        except IntegrityError as e:
            raise DataConflictError() from e
        if refresh:
            await self._s.refresh(model)
            return model

    async def delete(self, model: ModelT):
        await self._s.delete(model)
        await self._s.flush()

    async def delete_where(self, *filters) -> int:
        results = await self._run_query(delete(self.model).where(*filters), commit=True)
        self._s.expire_all()
        return results[0]
