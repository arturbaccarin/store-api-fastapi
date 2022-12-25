from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from typing import List

from core.dependencies import get_db
from models.seller import SellerModel
from schemas.seller import SellerSchema, SellerSchemaCreate
from core.security import get_current_active_user
from models.user import UserModel

router = APIRouter()


# GET sellers
@router.get("/", response_model=List[SellerSchema], status_code=status.HTTP_200_OK)
async def get_sellers(
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(SellerModel).order_by(SellerModel.id)
        result = await session.execute(query)
        sellers: List[SellerModel] = result.scalars().unique().all()

        return sellers


# GET seller
@router.get(
    "/{seller_id}",
    response_model=SellerSchema,
    response_model_exclude={"email", "id"},
    status_code=status.HTTP_200_OK,
)
async def get_sellers(
    seller_id: int,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(SellerModel).filter(SellerModel.id == seller_id)
        result = await session.execute(query)
        seller: SellerModel = result.scalars().unique().one_or_none()

        if seller:
            return seller
        else:
            raise HTTPException(
                detail="Seller hasn't been found", status_code=status.HTTP_404_NOT_FOUND
            )


# POST seller
@router.post(
    "/", response_model=SellerSchemaCreate, status_code=status.HTTP_201_CREATED
)
async def post_seller(
    seller: SellerSchemaCreate,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    new_seller = SellerModel(**seller.dict())
    seller_name = new_seller.name

    try:
        db.add(new_seller)
        await db.commit()
    except Exception as e:
        return JSONResponse({"detail": str(e)})

    return JSONResponse({"detail": f"Seller '{seller_name}' has been created!"})


# PUT seller
@router.put(
    "/{seller_id}",
    response_model=SellerSchemaCreate,
    status_code=status.HTTP_201_CREATED,
)
async def put_seller(
    seller_id: int,
    seller: SellerSchemaCreate,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):

    try:
        async with db as session:
            query = (
                sqlalchemy_update(SellerModel)
                .where(SellerModel.id == seller_id)
                .values(**seller.dict())
            )
            await session.execute(query)
            await session.commit()
            return seller

    except Exception as e:
        return JSONResponse({"detail": str(e)})


# DELETE seller
@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(
    seller_id: int,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(SellerModel).filter(SellerModel.id == seller_id)
        result = await session.execute(query)
        seller_del: SellerModel = result.scalars().unique().one_or_none()

        if seller_del:
            seller_name = seller_del.name
            await session.delete(seller_del)
            await session.commit()

            return JSONResponse({"detail": f"Seller '{seller_name}' has been deleted!"})
        else:
            raise HTTPException(
                detail="Seller hasn't been found", status_code=status.HTTP_404_NOT_FOUND
            )
