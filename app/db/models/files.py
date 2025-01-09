from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import JSON


@as_declarative()
class FilesEntityBase:
    files = Column(JSON(none_as_null=True), nullable=True)


__all__ = [
    "FilesEntityBase",
]
