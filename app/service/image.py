from io import BytesIO
from secrets import token_urlsafe
from typing import Literal
from uuid import uuid4

from urllib.parse import quote
from fastapi import UploadFile, File, HTTPException
from PIL import Image

from app.db.s3 import s3_client
from app.core.config import settings


class ImageFile:
    data: UploadFile | None = File(None)
    byte_data: bytes | None = None

    def __init__(self, data: UploadFile):
        self.data = data

    def extension(self) -> str:
        return self.data.filename.split(".")[-1]

    async def validate(self) -> bool:
        return self.validate_type() and await self.validate_size()

    def validate_type(self) -> bool:
        if self.extension().lower() not in ["jpg", "jpeg", "png"]:
            return False
        return True

    async def validate_size(self) -> bool:
        if len(self.byte_data) > 10 * 1024 * 1024:
            return False
        return True

    async def upload_to_s3(
        self, user_id: int, directory: Literal["debate", "post", "summary"]
    ) -> str:
        """
        1. Check if extension is available
        2. Check if size if acceptable
        3. Change name of image
        4. Optimize image and save
        """
        await self.to_bytes()
        if not await self.validate():
            raise HTTPException(status_code=413)
        filename = f"{user_id}_{str(uuid4())}.{self.extension()}"
        try:
            s3_client.upload_fileobj(
                BytesIO(self.byte_data),
                settings.AWS_S3_BUCKET_NAME,
                f"{directory}/{filename}",
                ExtraArgs={"ContentType": self.data.content_type},
            )
            return f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{quote(f"{directory}/{filename}", safe="~()*!.'")}"
        except Exception as e:
            print(e)
            return str(e)

    async def to_bytes(self) -> BytesIO:
        self.byte_data = await self.data.read()
