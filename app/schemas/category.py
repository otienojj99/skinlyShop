from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name:Optional[str]
    
class CategoryRead(CategoryBase):
    id: int
    slug: str
    shop_id: int

    class Config:
        from_attributes = True