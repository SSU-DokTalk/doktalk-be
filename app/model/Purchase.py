from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.db.soft_delete import SoftDeleteMixin


class Purchase(Base, Timestamp, SoftDeleteMixin):
    __tablename__ = "purchase"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreatePurchaseReq":
            user = kwargs["user"]
            purchase_data = kwargs["data"]
            self.user_id = user.id
            self.product_id = purchase_data.product_type + str(purchase_data.product_id)
            self.content = purchase_data.content
            self.price = purchase_data.price
            self.quantity = purchase_data.quantity

    # Keys
    id = Column(INTEGER(unsigned=True), primary_key=True)
    user_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    ## - 구분: (D: Debate, S: Summary) // 1자리
    ## - 상품 id: BIGINT(unsigned=True) // 최대 20자리
    ## product_id = 구분 + 상품 id // 최대 21자리
    product_id = Column(VARCHAR(21), nullable=False, index=True)
    ## 구매 내역 설명
    content = Column(VARCHAR(255), nullable=False)
    ## 개당 구매 가격
    price = Column(INTEGER, nullable=False)
    ## 구매 수량
    quantity = Column(INTEGER, nullable=False)

    ## is_deleted: BOOLEAN // 환불 여부

    # Relationships
