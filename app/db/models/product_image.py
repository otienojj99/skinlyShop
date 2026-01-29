# app/db/models/product_image.py
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_main = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())