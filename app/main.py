from fastapi import FastAPI
# app/main.py
import app.core.cloudinary
from app.api.v1.router import api_router
from app.api.v1.shop import router
from app.api.v1.products import prouter
from app.api.v1.category import crouter
from app.api.v1.inventory import irouter
from app.api.v1.discount import drouter
from app.api.v1.product_images import mrouter
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(router)
app.include_router(crouter)
app.include_router(prouter)
app.include_router(irouter)
app.include_router(drouter)
app.include_router(mrouter)



