from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate
from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService
from app.api.deps import require_shop_owner


irouter = APIRouter(prefix="/products/{product_id}/inventory",tags=["inventory"])

@irouter.post( "/", response_model=InventoryRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_shop_owner)])
async def create_inventory(product_id: int,inventory_in: InventoryCreate,db: AsyncSession = Depends(get_db),):
    inventory_service = InventoryService(db)
    product = await ProductService(db).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = await inventory_service.get_by_product(product_id)
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    
    service = InventoryService(db)
    return await service.create(product_id, inventory_in.quantity)

@irouter.get("/", response_model=InventoryRead)
async def get_inventory(product_id: int, db: AsyncSession = Depends(get_db)):
    service = InventoryService(db)
    inventory = await service.get_by_product(product_id)
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@irouter.put("/", response_model=InventoryRead, dependencies=[Depends(require_shop_owner)])
async def update_inventory(product_id: int, inventory_in: InventoryUpdate, db: AsyncSession = Depends(get_db), user=Depends(require_shop_owner),):
    service = InventoryService(db)
    inventory = await service.get_by_product(product_id)
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return await service.update(
        inventory,
        inventory_in.dict(exclude_unset=True)
    )