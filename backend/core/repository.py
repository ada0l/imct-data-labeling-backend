import abc
from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import Base
from backend.core.schemas import PaginationPydantic

Model = TypeVar("Model", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseRepository(
    Generic[Model, Schema, CreateSchema, UpdateSchema], metaclass=abc.ABCMeta
):
    @property
    @abc.abstractmethod
    def _model(self) -> Type[Model]:
        ...

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_query(self):
        return select(self._model)  # type: ignore

    async def create(
        self, schema_in: CreateSchema, commit: bool = True, **additional_fields
    ) -> Model:
        db_obj = self._model(**schema_in.dict(), **additional_fields)  # type: ignore
        self.session.add(db_obj)
        if commit:
            await self.session.commit()
            await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, obj_id: int) -> Model:
        q = await self.session.execute(
            self.get_query().filter(self._model.id == obj_id)  # type: ignore
        )
        return q.scalars().first()

    async def get_multi(
        self, pagination: PaginationPydantic | None = None
    ) -> list[Model]:
        if pagination:
            q = await self.session.execute(
                self.get_query()
                .limit(pagination.limit)
                .offset(pagination.offset)
            )
        else:
            q = await self.session.execute(self.get_query())
        return q.scalars().all()

    async def update(
        self, obj: Model, obj_in: UpdateSchema, commit: bool = True
    ) -> Model:
        obj_data = jsonable_encoder(obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        self.session.add(obj)
        if commit:
            await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete_by_id(self, obj_id: int, commit: bool = True) -> Model:
        obj = await self.get_by_id(obj_id=obj_id)
        return await self.delete(obj=obj, commit=commit)

    async def delete(self, obj: Model, commit: bool = True) -> Model:
        await self.session.delete(obj)
        if commit:
            await self.session.commit()
        return obj
