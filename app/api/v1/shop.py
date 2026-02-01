from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.shop import ShopCreate, ShopRead, ShopUpdate
from app.api.deps import require_shop_owner
from app.services.shop_service import ShopServices


router = APIRouter(prefix="/shops", tags=["shops"])

@router.post("/", response_model=ShopRead, dependencies=[Depends(require_shop_owner)])
async def create_shop(shop_in: ShopCreate, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner)):
    service = ShopServices(db)
    return await service.create(owner_id=user["sub"], shop_data=shop_in.dict())


@router.get("/{shop_id},", response_model=ShopRead)
async def get_shop(shop_id: int, db: AsyncSession = Depends(get_db)):
    service = ShopServices(db)
    shop = await service.get(shop_id)
    if not shop:
         raise HTTPException(status_code=404, detail="Shop not found")
    return shop

@router.put("/{shop_id}", response_model=ShopRead, dependencies=[Depends(require_shop_owner)])
async def update_shop(shop_id: int, shop_in: ShopUpdate, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner)):
    service = ShopServices(db)
    shop = await service.get(shop_id)
    if not shop:
         raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != user["sub"]:
         raise HTTPException(status_code=403, detail="Not allowed")
    return await service.update(shop, shop_in.dict(exclude_unset=True))

@router.get("/", response_model=List[ShopRead])
async def list_shops(db: AsyncSession = Depends(get_db)):
    service = ShopServices(db)
    return await service.list()


@router.get("/slug/{slug}", response_model=ShopRead)
async def get_shop_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    service = ShopServices(db)
    shop = await service.get_by_slug(slug) 
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop

@router.get("/owner/me", response_model=List[ShopRead], dependencies=[Depends(require_shop_owner)])
async def get_my_shops(db: AsyncSession = Depends(get_db),
    user=Depends(require_shop_owner),):
    service = ShopServices(db)
    return await service.get_by_owner(owner_id=user["sub"])


@router.delete("/{shop_id}", status_code=204, dependencies=[Depends(require_shop_owner)])
async def delete_shop(shop_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_shop_owner),):
    service = ShopServices(db)
    
    shop = await service.get(shop_id)
    if not shop:
         raise HTTPException(status_code=404, detail="Shop not found")
    if shop.owner_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    await service.delete(shop)
    return None
