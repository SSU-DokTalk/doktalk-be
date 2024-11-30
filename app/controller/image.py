from typing import Literal, Annotated

from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import oauth2_scheme
from app.service.image import ImageFile

router = APIRouter()


@router.post("")
async def uploadImage(
    file: UploadFile,
    directory: Literal["debate", "post", "summary"],
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> str:
    image = ImageFile(file)
    url = await image.upload_to_s3(request.state.user.id, directory)
    return url
