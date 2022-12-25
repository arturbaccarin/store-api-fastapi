from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy import update as sqlalchemy_update
from schemas.token import Token
from typing import List
from datetime import timedelta

from core.dependencies import get_db
from models.user import UserModel
from schemas.user import UserSchema, UserSchemaCreate, UserSchemaPassword
from core.security import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user,
)


router = APIRouter()


# POST signup
@router.post("/signup", response_model=UserSchema)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    new_user: UserModel = UserModel(
        name=user.name, email=user.email, password=get_password_hash(user.password)
    )

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()
            return new_user

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="There is already a user with this registered email.",
            )


# GET token/login
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# GET users
@router.get("/", response_model=List[UserSchema])
async def get_users(
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(UserModel).order_by(UserModel.id)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().unique().all()
        return users


# GET user
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()
        if user:
            return user
        else:
            raise HTTPException(
                detail="User hasn't been found", status_code=status.HTTP_404_NOT_FOUND
            )


# DELETE user
@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserModel = result.scalars().unique().one_or_none()

        if user_del:
            user_name = user_del.name
            await session.delete(user_del)
            await session.commit()

            return JSONResponse({"detail": f"Seller '{user_name}' has been deleted!"})
        else:
            raise HTTPException(
                detail="Seller hasn't been found", status_code=status.HTTP_404_NOT_FOUND
            )


# PUT password
@router.put("/updatePassword")
async def put_password(
    password: UserSchemaPassword,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    plain_password: str = password.password

    async with db as session:
        logged_user.password = get_password_hash(plain_password)
        session.add(logged_user)
        await session.commit()
        return JSONResponse({"detail": "Password updated!"})


# PUT user
@router.put(
    "/{user_id}", response_model=UserSchema, response_model_exclude={"id", "disabled"}
)
async def put_user(
    user_id: int,
    user: UserSchema,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    try:
        async with db as session:
            query = (
                sqlalchemy_update(UserModel)
                .where(UserModel.id == user_id)
                .values(**user.dict())
            )
            await session.execute(query)
            await session.commit()
            return user

    except Exception as e:
        return JSONResponse({"detail": str(e)})


# GET me
# @router.get("/me", response_model=UserSchema)
# async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
#     return current_user
