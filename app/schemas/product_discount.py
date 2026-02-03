from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductDiscountBase(BaseModel):
    discount_type: str
    discount_value: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProductDiscountCreate(ProductDiscountBase):
    product_id: int
    


class DiscountUpdate(BaseModel):
    discount_type: Optional[str]
    discount_value: Optional[Decimal]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_active: Optional[bool]
    
class ProductDiscountRead(ProductDiscountBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
    