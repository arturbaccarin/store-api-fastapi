from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session


async def get_db():
    db: AsyncSession = Session()

    try:
        yield db
    finally:
        await db.close()
