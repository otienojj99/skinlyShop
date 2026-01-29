# app/db/models/product.py
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)       # links to Shop
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  # optional category
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    discount = Column(JSON, default={})       # e.g., {"type":"PERCENT","value":10,"start_date":"2026-02-01","end_date":"2026-02-10"}
    attributes = Column(JSON, default={})     # e.g., {"skin_types":["oily","dry"],"concerns":["acne"],"ingredients":["niacinamide"]}
    status = Column(String(20), default="ACTIVE")   # ACTIVE | OUT_OF_STOCK | HIDDEN
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())