import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class SlugHelper:
    def __init__(self, db: AsyncSession, model):
         self.db = db
         self.model = model
         
         
    def slugify(self, text: str)->str:
        slug = text.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        
        return slug.strip("_")
    
    async def generate_unique_slug(self, base_text: str)->str:
        base_slug = self.slugify(base_text)
        slug = base_slug
        counter = 1
        
        while True:
            result = await self.db.execute(
             select(self.model).where(self.model.slug == slug)
            )
            exists = result.scalar_one_or_none()
            
            if not exists:
                return slug
            
            slug = f"{base_slug}-{counter}"
            counter += 1