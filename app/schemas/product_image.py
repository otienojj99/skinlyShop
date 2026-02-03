# app/schemas/product_image.py
from pydantic import BaseModel
from datetime import datetime


class ProductImageBase(BaseModel):
    image_url: str
    is_main: bool = False


class ProductImageCreate(BaseModel):
    is_main: bool = False


class ProductImageRead(ProductImageBase):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True
