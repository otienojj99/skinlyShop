from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.inventory import Inventory
from app.db.models.product import Product


class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create(self, product_id: int, quantity: int)->Inventory:
        inventory = Inventory(
            product_id = product_id,
            quantity = quantity
        )
        self.db.add(inventory)
        await self.db.commit()
        await self.db.refresh(inventory)
        return inventory
    
    async def get_by_product(self, product_id: int)-> Inventory | None:
        result = await self.db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        
        return result.scalar_one_or_none()
    
    async def update(self, inventory: Inventory, updates: dict)-> Inventory:
        for key, value in updates.items():
            setattr(inventory, key, value)
            
        await self.db.commit()
        await self.db.refresh(inventory)
        return inventory
    
    async def adjust_quantity(self, inventory: Inventory, delta: int)-> Inventory:
        inventory.quantity += delta
        
        if inventory.quantity == 0:
            raise ValueError("Out of stock")
        
        if inventory.quantity < 1 and inventory.quantity == 10:
            raise ValueError("Running out of stock")
        
        await self.db.commit()
        await self.db.refresh(inventory)
        return inventory