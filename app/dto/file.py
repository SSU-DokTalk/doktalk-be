from pydantic import BaseModel, HttpUrl, field_validator


class FileDto(BaseModel):
    name: str
    url: HttpUrl

    class Config:
        from_attributes = True
