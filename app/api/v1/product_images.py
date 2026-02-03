from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.models.product_image import ProductImage
from app.db.session import get_db
from app.api.deps import require_shop_owner
from app.services.product_service import ProductService
from app.services.product_image_service import ProductImageService
from app.schemas.product_image import ProductImageCreate, ProductImageRead

mrouter = APIRouter(
    prefix="/products/{product_id}/images",
    tags=["product-images"],
)

@mrouter.post("/", response_model=ProductImageRead)
async def upload_product_image(product_id: int,file: UploadFile = File(...),is_main: bool = False,db: AsyncSession = Depends(get_db),user=Depends(require_shop_owner),):
    product_service = ProductService(db)
    image_service = ProductImageService(db)
    
    product = await product_service.get(product_id)
    if not product:
         raise HTTPException(status_code=404, detail="Product not found")
     
    if not product.shop.owner_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await image_service.add_image(
        product_id=product_id,
        file=file.file,
        is_main=is_main,
    )

@mrouter.get("/", response_model=List[ProductImageRead])
async def list_product_images(product_id: int,db: AsyncSession = Depends(get_db),):
    image_service = ProductImageService(db)
    return await image_service.list_by_product(product_id)

@mrouter.delete("/{image_id}", status_code=204)
async def delete_product_image( product_id: int,image_id: int,db: AsyncSession = Depends(get_db),user=Depends(require_shop_owner),):
    image_service = ProductImageService(db)
    
    image = await db.get(ProductImage, image_id)
    
    if not image or image.product_id != product_id:
        raise HTTPException(status_code=404, detail="Image not found")
    
    await image_service.delete(image)