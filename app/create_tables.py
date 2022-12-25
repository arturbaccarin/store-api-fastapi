from core.settings import settings
from core.database import engine


async def create_tables() -> None:
    import models.department
    import models.seller
    import models.user

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_tables())
