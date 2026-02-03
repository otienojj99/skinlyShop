from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.products import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService
from app.api.deps import require_shop_owner

prouter = APIRouter(
    prefix="/shops/{shop_id}/products",
    tags=["products"]
)

@prouter.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_shop_owner)])
async def create_product(shop_id: int, product_in: ProductCreate, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner)):
    service = ProductService(db)
    try:
        return await service.create(
            shop_id=shop_id,
            product_data=product_in.dict()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@prouter.get("/", response_model=List[ProductRead])
async def list_products(shop_id: int,db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.list_by_shop(shop_id)

@prouter.get("/slug/{slug}", response_model=ProductRead)
async def get_product_by_slug(shop_id: int, slug: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get_by_slug(shop_id, slug)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@prouter.get("/{product_id}", response_model=ProductRead)
async def get_product(shop_id: int, product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get(product_id)
    
    if not product or product.shop_id != shop_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    return product

@prouter.put("/{product_id}", response_model=ProductRead, dependencies=[Depends(require_shop_owner)])
async def update_product(shop_id: int, product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner),):
    service = ProductService(db)
    product = await service.get(product_id)
    
    if not product or product.shop_id != shop_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return await service.update(product, product_in.dict(exclude_unset=True))

@prouter.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_shop_owner)])
async def delete_product(shop_id: int, product_id: int, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner)):
    service = ProductService(db)
    product = await service.get(product_id)
    
    if not product or product.shop_id != shop_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
        
    await service.delete(product)
    