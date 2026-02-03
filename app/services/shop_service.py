# app/services/shop_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.shop import Shop
from typing import List
from app.helpers.slug_helper import SlugHelper



class ShopServices:
    
    def __init__(self, db:AsyncSession):
        self.db = db
        self.slug_helper = SlugHelper(db, Shop)
        
        # Creating shop
    async def create(self, owner_id: int, shop_data:dict)->Shop:
        slug = await self.slug_helper.generate_unique_slug(shop_data["name"])
        new_shop = Shop(owner_id=owner_id, slug=slug **shop_data)
        self.db.add(new_shop)
        await self.db.commit()
        await self.db.refresh(new_shop)
        return new_shop
    
    # Getting shop by id
    async def get(self, shop_id: int)->Shop | None:
        return await self.db.get(Shop, shop_id)
    
    # Update shop
    async def update(self, shop: Shop, updates: dict)-> Shop:
        for k, v in updates.items():
            setattr(shop, k, v)
        await self.db.commit()
        await self.db.refresh(shop)
        return shop
    
    async def delete(self, shop:Shop)->None:
        await self.db.delete(shop)
        return self.db.commit()
    
    # List all shops
    async def list(self)-> List[Shop]:
        result = await self.db.execute(select(Shop).order_by(Shop.created_at.desc()))
        return result.scalars().all()
    
    async def get_by_owner(self, owner_id: int)-> List[Shop]:
        result = await self.db.execute(
            select(Shop).where(Shop.owner_id == owner_id)
        )
        return result.scalars().all()
    
    
    async def search_by_name(self, query:str)-> List[Shop]:
        result = await self.db.execute(
            select(Shop).where(Shop.name.ilike(f"%{query}%"))
        )
        
        return result.scalars().all()
    
    
    async def get_by_slug(self, slug: str):
        stmt = select(Shop).where(Shop.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    