from typing import Union, Type
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import DATETIME, BOOLEAN
from sqlalchemy.orm import Session, Mapper
from sqlalchemy.orm.util import AliasedClass, AliasedInsp
from sqlalchemy.sql.type_api import _T, _O


_EntityType = Union[Type[_T], "AliasedClass[_T]", "Mapper[_T]", "AliasedInsp[_T]"]


class BaseSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def query(self, _entity: _EntityType[_O], with_deleted=False):
        if not hasattr(_entity, "is_deleted") or with_deleted:
            return super().query(_entity)
        return super().query(_entity).filter_by(is_deleted=False)


class SoftDeleteMixin:
    is_deleted = Column(BOOLEAN, nullable=False, default=False, server_default="0")
    deleted_at = Column(DATETIME, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None


__all__ = [
    "BaseSession",
    "SoftDeleteMixin",
]
