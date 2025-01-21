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
            Purchase.product_id == product_id,
            Purchase.product_type == product_type,
        )
        .first()
    )
    if purchase == None:
        raise HTTPException(status_code=404)
    return purchase


def createPurchaseService(
    user_id: int, purchase_data: CreatePurchaseReq, db: Session
) -> int:
    try:
        purchase_history = (
            db.query(Purchase)
            .filter(
                Purchase.user_id == user_id,
                Purchase.product_id == purchase_data.product_id,
                Purchase.product_type == purchase_data.product_type,
            )
            .first()
        )
        if purchase_history != None:
            raise HTTPException(status_code=409)

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
        purchase = Purchase(user_id=user_id, data=purchase_data)

        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase.id
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400)


def deletePurchaseService(user_id: int, purchase_id: int, db: Session) -> None:
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if purchase == None:
        raise HTTPException(status_code=404)
    if purchase.user_id != user_id:
        raise HTTPException(status_code=403)
    purchase.soft_delete()
    db.commit()
    return


__all__ = [
    "getPurchasesService",
    "getPurchaseService",
    "createPurchaseService",
    "deletePurchaseService",
]
