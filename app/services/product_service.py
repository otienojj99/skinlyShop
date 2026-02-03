from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List
from app.db.models.product import Product
from app.helpers.slug_helper import SlugHelper
from app.helpers.discount_helper import DiscountHelper


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, shop_id: int, product_data: dict) -> Product:
        slug = SlugHelper.generate_unique_slug(
            product_data["name"],
            scope={"shop_id": shop_id}
        )

        product = Product(
            **product_data,
            shop_id=shop_id,
            slug=slug
        )

        self.db.add(product)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Product with same name already exists in this shop")

        await self.db.refresh(product)
        return product

    async def get(self, product_id: int) -> Product | None:
        return await self.db.get(Product, product_id)

    async def get_by_slug(self, shop_id: int, slug: str) -> Product | None:
        result = await self.db.execute(
            select(Product).where(
                Product.shop_id == shop_id,
                Product.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def list_by_shop(self, shop_id: int) -> List[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.shop_id == shop_id)
            .order_by(Product.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, product: Product, updates: dict) -> Product:
        if "name" in updates:
            updates["slug"] = SlugHelper.generate_unique_slug(
                updates["name"],
                scope={"shop_id": product.shop_id}
            )

        for key, value in updates.items():
            setattr(product, key, value)

        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()
