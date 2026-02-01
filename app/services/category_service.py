from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.category import Category
from app.helpers.slug_helper import SlugHelper




class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
       
    
    
    async def create(self, shop_id: int, name: str)->Category:
        slug = SlugHelper.generate_unique_slug(name)
        
        category = Category(
            name=name,
            slug=slug,
            shop_id=shop_id
        )
        
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    # Get by id
    async def get(self, category_id: int)->Category | None:
        return await self.db.get(Category, category_id)
    
    # Get by slug per shop
    
    async def get_by_slug(self, shop_id: int, slug: str)-> Category | None:
        result = await self.db.execute(
            select(Category).where(
                Category.shop_id == shop_id,
                Category.slug == slug
            )
        )
        return result.scalar_one_or_none()
    
    # List categories for a shop
    async def list_by_shop(self, shop_id: int) -> list[Category]:
        result = await self.db.execute(
            select(Category).where(Category.shop_id == shop_id).order_by(Category.created_at.desc())
        )
        
        return result.scalars().all()
    
    # Update category (regenerate slug if name changes)
    
    async def update(self, category: Category, updates: dict)->Category:
        if "name" in updates:
            updates["slug"] = SlugHelper.generate(updates["name"])
            
        for key, value in updates.items():
            setattr(category, key, value)
            
        await self.db.commit
        await self.db.refresh(category)
        return category
    
    
      # Delete category
    async def delete(self, category: Category) -> None:
        await self.db.delete(category)
        await self.db.commit()