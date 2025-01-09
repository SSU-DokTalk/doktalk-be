from io import BytesIO
from typing import Literal
from uuid import uuid4

from urllib.parse import quote, unquote
from fastapi import UploadFile, File, HTTPException

from app.db.s3 import s3_client
from app.core.config import settings


prefix = (
    f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/"
)


class FileManager:
    data: UploadFile | None = File(None)
    byte_data: bytes | None = None

    def __init__(self, data: UploadFile):
        self.data = data

    def extension(self) -> str:
        """
        이미지 파일의 확장자 반환
        """
        return self.data.filename.split(".")[-1].lower()

    async def validate(self) -> bool:
        return self.validate_type() and await self.validate_size()

    def validate_type(self) -> bool:
        """
        이미지 파일의 확장자가 acceptable한지 확인
        """
        if self.extension().lower() not in ["jpg", "jpeg", "png", "gif", "pdf"]:
            raise HTTPException(status_code=415)
        return True

    async def validate_size(self) -> bool:
        """
        이미지 파일의 크기가 10MB를 넘지 않는지 확인
        """
        if len(self.byte_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413)
        return True

    async def upload_to_s3(
        self, user_id: int, directory: Literal["debate", "post", "summary", "profile"]
    ) -> str:
        """
        1. Check if extension is available
        2. Check if size if acceptable
        3. Change name of image
        4. Optimize image and save
        """
        await self.to_bytes()
        if not await self.validate():
            raise HTTPException(status_code=400)
        filename = f"{user_id}_{str(uuid4())}.{self.extension()}"
        try:
            s3_client.upload_fileobj(
                BytesIO(self.byte_data),
                settings.AWS_S3_BUCKET_NAME,
                f"{directory}/{filename}",
                ExtraArgs={"ContentType": self.data.content_type},
            )
            return f"{prefix}{quote(f"{directory}/{filename}", safe="~()*!.'")}"
        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    async def delete_from_s3(file_path: str) -> bool:
        """
        S3 버킷에서 파일 삭제
        Args:
            file_path (str): S3 내의 파일 경로 (예: f'{prefix}directory/filename.jpg')

        Returns:
            bool: 성공 시 True, 실패 시 False
        """
        if (
            not file_path
            or len(file_path) < len(prefix)
            or file_path[: len(prefix)] != prefix
        ):
            return False

        file_path = unquote("/".join(file_path.split("/")[3:]))
        try:
            s3_client.delete_object(Bucket=settings.AWS_S3_BUCKET_NAME, Key=file_path)
            return True
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400)

    async def to_bytes(self) -> BytesIO:
        self.byte_data = await self.data.read()


__all__ = [
    "FileManager",
]
