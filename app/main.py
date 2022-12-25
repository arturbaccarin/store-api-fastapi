from fastapi import FastAPI
from api.v1.api import api_router
from core.settings import settings


app = FastAPI(title="Store")

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Hello Department Application!"}


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
