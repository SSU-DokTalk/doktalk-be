from fastapi import APIRouter, Depends

from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.model import MyBook, User
from app.service.my_book import addMyBookService


router = APIRouter()

###########
### GET ###
###########


############
### POST ###
############
def addMyBookController(
    user_id: int,
    isbn: int,
    db: Session = Depends(get_db),
):
    return addMyBookService(user_id, isbn, db)


###########
### PUT ###
###########

#############
### PATCH ###
#############

##############
### DELETE ###
##############
