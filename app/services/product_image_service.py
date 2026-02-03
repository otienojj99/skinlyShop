# app/services/product_image_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models.product_image import ProductImage
from app.helpers.image_helper import ImageHelper


class ProductImageService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_image(self,product_id: int,file,is_main: bool = False,)->ProductImage:
        upload = ImageHelper.upload_product_image(file)
        
        if is_main:
            await self.db.execute(
                update(ProductImage)
                .where(ProductImage.product_id == product_id)
                .values(is_main=False)
            )
            
        image = ProductImage(
            product_id=product_id,
            image_url = upload["url"],
            public_id=upload["public_id"],
            is_main=is_main,
        )
        
        await self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image
    
    async def list_by_product(self, product_id: int):
        result = await self.db.execute(
            select(ProductImage)
            .where(ProductImage.product_id == product_id)
            .order_by(ProductImage.is_main.desc())
        )
        
        return result.scalars().all()
    
    async def delete(self, image: ProductImage):
        ImageHelper.delete_image(image.public_id)
        await self.db.delete(image)
        await self.db.commit()