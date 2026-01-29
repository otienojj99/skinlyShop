# app/db/models/product_discount.py
from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class ProductDiscount(Base):
    __tablename__ = "product_discounts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    type = Column(String(20), nullable=False)      # PERCENT | FLAT
    value = Column(Numeric(10,2), nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())