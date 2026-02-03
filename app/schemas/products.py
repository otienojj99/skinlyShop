from pydantic import BaseModel
from typing import Optional, Dict, Any
from decimal import Decimal
from datetime import datetime



class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    currency: Optional[str] = "KES"
    category_id: Optional[int] = None
    discount: Optional[Dict[str, Any]] =  None
    attributes: Optional[Dict[str, Any]] =  None
    status: Optional[str] = "ACTIVE"
    
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    currency: Optional[str]
    category_id: Optional[int]
    discount: Optional[Dict[str, Any]]
    attributes: Optional[Dict[str, Any]]
    status: Optional[str]


class ProductRead(ProductBase):
    id: int
    shop_id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


