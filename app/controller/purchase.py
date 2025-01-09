from typing import Annotated, Literal

from fastapi.security import HTTPAuthorizationCredentials
from fastapi import APIRouter, Depends, Request

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.dto.purchase import CreatePurchaseReq
from app.schema.purchase import PurchaseSchema
from app.service.purchase import *

router = APIRouter()


###########
### GET ###
###########
@router.get("/{product_type}/{product_id}")
def getPurchaseController(
    request: Request,
    product_type: Literal["D", "S"],
    product_id: int,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> PurchaseSchema:
    """
    유저 본인이 해당 상품을 구매했는지 여부 조회
    """
    return getPurchaseService(request.state.user.id, product_type, product_id, db)


############
### POST ###
############
@router.post("")
def createPurchaseController(
    request: Request,
    purchase_data: CreatePurchaseReq,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    구매 내역 생성
    """
    return createPurchaseService(request.state.user, purchase_data, db)


###########
### PUT ###
###########

#############
### PATCH ###
#############


##############
### DELETE ###
##############
@router.delete("/{purchase_id}")
def deletePurchaseController(
    request: Request,
    purchase_id: int,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    환불하기
    """
    return deletePurchaseService(request.state.user.id, purchase_id, db)
