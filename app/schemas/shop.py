from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime


class ShopBase(BaseModel):
    name:str
    description: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    location: Optional[str] = None
    website_url: Optional[str] = None
    social_links: Optional[Dict[str, str]] = {}
    
class ShopCreate(ShopBase):
    pass

class ShopUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    contact_email: Optional[EmailStr]
    contact_phone: Optional[str]
    location: Optional[str]
    website_url: Optional[str]
    social_links: Optional[Dict[str, str]]
    
class ShopRead(ShopBase):
    id:int
    owner_id:int
    slug: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes =True