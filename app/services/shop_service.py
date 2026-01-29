# app/services/shop_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.shop import Shop



class ShopServices:
    def __init__(self, db:AsyncSession):
        self.db = db
        
        # Creating shop
    async def create(self, owner_id: int, shop_data:dict)->Shop:
        new_shop = Shop(owner_id=owner_id, **shop_data)
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
    
    # List all shops
    async def list(self)-> list[Shop]:
        result = await self.db.execute("SELECT * FROM shops ORDER BY created_at DESC")
        return result.scalars().all()