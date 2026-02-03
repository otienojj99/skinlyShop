from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.db.models.product_discount import ProductDiscount
from app.helpers.discount_helper import DiscountHelper

class DiscountService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create(self,product_id: int,discount_data: dict)->ProductDiscount:
        DiscountHelper.validate_discount(
            discount_data["discount_type"],
            discount_data["discount_value"],
        )
        
        discount = ProductDiscount(
            product_id=product_id,
            **discount_data
        )
        
        self.db.add(discount)
        await self.db.commit()
        await self.db.refresh(discount)
        return discount
    
    async def get(self, discount_id: int) -> Optional[ProductDiscount]:
        return await self.db.get(ProductDiscount, discount_id)
    
    async def get_by_product(self, product_id: int) -> List[ProductDiscount]:
        result = await self.db.execute(
            select(ProductDiscount)
            .where(ProductDiscount.product_id == product_id)
            .order_by(ProductDiscount.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_active_discount(
        self,
        product_id: int
    ) -> Optional[ProductDiscount]:
        result = await self.db.execute(
            select(ProductDiscount)
            .where(ProductDiscount.product_id == product_id)
            .where(ProductDiscount.is_active == True)
            .order_by(ProductDiscount.created_at.desc())
        )
        
        discounts = result.scalars().all()
        
        for discount in discounts:
            if DiscountHelper.is_discount_active(
                discount.is_active,
                discount.start_date,
                discount.end_date,
            ):
                return discount
            
        return None
    
    async def update(
        self,
        discount: ProductDiscount,
        updates: dict
    ) -> ProductDiscount:
        
        if "discount_type" in updates or "discount_value" in updates:
             DiscountHelper.validate_discount(
                updates.get("discount_type", discount.discount_type),
                updates.get("discount_value", discount.discount_value),
            )
             
        for key, value in updates.items():
            setattr(discount, key, value)
            
        await self.db.commit()
        await self.db.refresh(discount)
        return discount
    
    async def delete(self, discount: ProductDiscount) -> None:
        await self.db.delete(discount)
        await self.db.commit()

