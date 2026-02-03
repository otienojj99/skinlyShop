# app/db/models/product.py
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, JSON, TIMESTAMP, Enum
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)       # links to Shop
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  # optional category
    name = Column(String(150), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    currency = Column(String(10), default="KES")
    # discount = Column(JSON, default=dict)       # e.g., {"type":"PERCENT","value":10,"start_date":"2026-02-01","end_date":"2026-02-10"}
    attributes = Column(JSON, default=dict)     # e.g., {"skin_types":["oily","dry"],"concerns":["acne"],"ingredients":["niacinamide"]}
    status = Column(
    Enum(
        "ACTIVE",
        "OUT_OF_STOCK",
        "HIDDEN",
        name="product_status"
    ),
    nullable=False,
    default="ACTIVE"
)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    category = relationship("Category", back_populates="products")
    shop = relationship("Shop", back_populates="products")
    inventory = relationship("Inventory",uselist=False,back_populates="product",cascade="all, delete-orphan"
      )
    discounts = relationship(
    "ProductDiscount",
    back_populates="product",
    cascade="all, delete-orphan"
    )

