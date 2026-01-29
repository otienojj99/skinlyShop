import asyncio
from app.db.session import engine
from app.db.base import Base
from app.db.models import users, shop, category, product, inventory, product_image, product_discount


async def test_connection():
    async with engine.begin() as conn:
         await conn.run_sync(Base.metadata.create_all)  # creates tables if not exist
         
    print("✅ DB connected and tables synced!")
asyncio.run(test_connection())