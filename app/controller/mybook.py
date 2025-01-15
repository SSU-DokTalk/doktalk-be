from typing import Annotated, Union, List

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.service.my_book import *


router = APIRouter()


###########
### GET ###
###########
@router.get("s/is_in_library")
def isInLibraryController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    ids: Union[List[int], None] = Query(default=None),
    db: Session = Depends(get_db),
):
    return isInLibraryService(request.state.user.id, ids, db)


############
### POST ###
############
@router.post("/{isbn}")
def addMyBookController(
    isbn: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    return addMyBookService(request.state.user.id, isbn, db)


###########
### PUT ###
###########

#############
### PATCH ###
#############


##############
### DELETE ###
##############
@router.delete("/{isbn}")
def deleteMyBookController(
    isbn: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    return deleteMyBookService(request.state.user.id, isbn, db)
