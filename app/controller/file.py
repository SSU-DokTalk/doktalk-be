from typing import Literal, Annotated

from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import oauth2_scheme
from app.service.file import FileManager
from app.dto.file import FileDto

router = APIRouter()


@router.get("")
async def getFile(
    url: str,
):
    result = await FileManager.download_from_s3(url)
    return result


@router.post("")
async def uploadFile(
    file: UploadFile,
    directory: Literal["debate", "post", "summary", "profile"],
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> FileDto:
    image = FileManager(file)
    url = await image.upload_to_s3(request.state.user.id, directory)
    return url
