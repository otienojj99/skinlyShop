# app/db/models/product_image.py
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True,)
    image_url = Column(String, nullable=False)
    public_id = Column(String(255), nullable=False)   # Cloudinary ID
    is_main = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    product = relationship("Product", back_populates="images")