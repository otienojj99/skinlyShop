from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.product_discount import ProductDiscountCreate, ProductDiscountRead, DiscountUpdate
from app.db.session import get_db
from app.api.deps import require_shop_owner
from app.services.product_service import ProductService
from app.services.discount_service import DiscountService


drouter = APIRouter(prefix="/products/{product_id}/discounts",tags=["discounts"],)

drouter.post("/", response_model=ProductDiscountRead)
async def create_discount(
    product_id: int,
    discount_in: ProductDiscountCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_shop_owner),
):
    product_service = ProductService(db)
    discount_service = DiscountService(db)

    product = await product_service.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.shop.owner_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return await discount_service.create(
        product_id=product_id,
        discount_data=discount_in.dict(),
    )
    
@drouter.get("/", response_model=List[ProductDiscountRead])
async def list_product_discounts(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    discount_service = DiscountService(db)
    return await discount_service.get_by_product(product_id)


@drouter.get("/active", response_model=ProductDiscountRead | None)
async def get_active_discount(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    discount_service = DiscountService(db)
    return await discount_service.get_active_discount(product_id)



@drouter.put("/{discount_id}", response_model=ProductDiscountRead)
async def update_discount(
    product_id: int,
    discount_id: int,
    discount_in: DiscountUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_shop_owner),
):
    discount_service = DiscountService(db)
    product_service = ProductService(db)

    product = await product_service.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.shop.owner_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    discount = await discount_service.get(discount_id)
    if not discount or discount.product_id != product_id:
        raise HTTPException(status_code=404, detail="Discount not found")

    return await discount_service.update(
        discount,
        discount_in.dict(exclude_unset=True),
    )
    
    
@drouter.delete("/{discount_id}", status_code=204)
async def delete_discount(
    product_id: int,
    discount_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_shop_owner),
):
    discount_service = DiscountService(db)
    product_service = ProductService(db)

    product = await product_service.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.shop.owner_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    discount = await discount_service.get(discount_id)
    if not discount or discount.product_id != product_id:
        raise HTTPException(status_code=404, detail="Discount not found")

    await discount_service.delete(discount)




