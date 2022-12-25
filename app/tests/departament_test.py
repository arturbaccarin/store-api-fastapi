# from main import app
# from httpx import AsyncClient
# import pytest

# import asyncio


# @pytest.mark.anyio
# async def test_read_departments():
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     async with AsyncClient(app=app, base_url='http://localhost:8000') as ac:
#          response = await ac.get('/api/v1/departments/')
#     # assert response.status_code == 200
