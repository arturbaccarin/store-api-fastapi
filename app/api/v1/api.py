from fastapi import APIRouter

from api.v1.endpoints import department, seller, user

api_router = APIRouter()

api_router.include_router(department.router, prefix="/departments", tags=["Department"])
api_router.include_router(seller.router, prefix="/sellers", tags=["Seller"])
api_router.include_router(user.router, prefix="/users", tags=["User"])
