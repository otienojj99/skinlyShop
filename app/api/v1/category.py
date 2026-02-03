from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.api.deps import require_shop_owner
from app.services.category_service import CategoryService


crouter = APIRouter(prefix="/shops/{shop_id}/categories", tags=["categories"])

@crouter.post("/", response_model=CategoryRead, dependencies=[Depends(require_shop_owner)])
async def create_category(shop_id: int, category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.create(
        shop_id=shop_id,
        name=category_in.name
    )
    
@crouter.get("/", response_model=List[CategoryRead])
async def list_categories( shop_id: int,
    db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.list_by_shop(shop_id)

@crouter.get("/slug/{slug}", response_model=CategoryRead)
async def get_category_by_slug(shop_id: int,slug: str,db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    category = await service.get_by_slug(shop_id, slug)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@crouter.put("/{category_id}", response_model=CategoryRead, dependencies=[Depends(require_shop_owner)])
async def update_category(shop_id: int, category_id: int, category_in: CategoryUpdate, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner)):
    service = CategoryService(db)
    category = await service.get(category_id)
    
    if not category or category.shop_id != shop_id:
        raise HTTPException(status_code=404, detail="Category not found")
    return await service.update(category, category_in.dict(exclude_unset=True))


@crouter.delete("/{category_id}", status_code=204, dependencies=[Depends(require_shop_owner)])
async def delete_category(shop_id: int, category_id: int, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner)):
    service = CategoryService(db)
    category = await service.get(category_id)
    
    if not category or category.shop_id != shop_id:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await service.delete(category)