from typing import Literal, Annotated

from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import oauth2_scheme
from app.service.file import FileManager

router = APIRouter()


@router.post("")
async def uploadFile(
    file: UploadFile,
    directory: Literal["debate", "post", "summary", "profile"],
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> str:
    image = FileManager(file)
    url = await image.upload_to_s3(request.state.user.id, directory)
    return url
