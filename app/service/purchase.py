from typing import List, Literal

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.dto.purchase import CreatePurchaseReq
from app.db.models.soft_delete import BaseSession as Session
from app.model.Purchase import Purchase
from app.model.User import User
from app.model.Debate import Debate
from app.model.Summary import Summary
from app.schema.purchase import PurchaseSchema


def getPurchasesService(user_id: int, db: Session) -> List[PurchaseSchema]:
    res = (
        db.query(Purchase, with_deleted=True)
        .filter(Purchase.user_id == user_id)
        .order_by(Purchase.created.desc())
        .all()
    )
    if res == None:
        raise HTTPException(status_code=404)
    return res


def getPurchaseService(
    user_id: int, product_type: Literal["D", "S"], product_id: int, db: Session
) -> PurchaseSchema:
    purchase = (
        db.query(Purchase)
        .filter(
            Purchase.user_id == user_id,
            Purchase.product_id == product_type + str(product_id),
        )
        .first()
    )
    if purchase == None:
        raise HTTPException(status_code=404)
    return purchase


def createPurchaseService(
    user: User, purchase_data: CreatePurchaseReq, db: Session
) -> int:
    try:
        if purchase_data.product_type == "D":
            debate = db.get(Debate, purchase_data.product_id)
            if debate == None:
                raise HTTPException(status_code=404)
        elif purchase_data.product_type == "S":
            summary = db.get(Summary, purchase_data.product_id)
            if summary == None:
                raise HTTPException(status_code=404)
        else:
            raise HTTPException(status_code=400)

        purchase = Purchase(user=user, data=purchase_data)
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase.id
    except IntegrityError as e:
        raise HTTPException(status_code=400)


def deletePurchaseService(user_id: int, purchase_id: int, db: Session) -> None:
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if purchase == None:
        raise HTTPException(status_code=404)
    if purchase.user_id != user_id:
        raise HTTPException(status_code=403)
    db.delete(purchase)
    db.commit()


__all__ = [
    "getPurchasesService",
    "getPurchaseService",
    "createPurchaseService",
    "deletePurchaseService",
]
