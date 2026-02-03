from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class  InventoryBase(BaseModel):
    quantity: int
    reserved_quantity: Optional[int] = 0

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int]
    reserved_quantity: Optional[int]
    
class InventoryRead(InventoryBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
       from_attributes = True