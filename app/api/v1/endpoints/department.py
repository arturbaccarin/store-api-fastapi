from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.security import get_current_active_user
from core.dependencies import get_db
from models.department import DepartmentModel
from schemas.department import DepartmentSchema, DepartmentSchemaCreate
from models.user import UserModel


router = APIRouter()


# GET departments
@router.get("/", response_model=List[DepartmentSchema], status_code=status.HTTP_200_OK)
async def get_departments(db: AsyncSession = Depends(get_db)):
    async with db as session:
        query = select(DepartmentModel).order_by(DepartmentModel.id)
        result = await session.execute(query)
        departments: List[DepartmentModel] = result.scalars().unique().all()

        return departments


# GET department
@router.get(
    "/{department_id}", response_model=DepartmentSchema, status_code=status.HTTP_200_OK
)
async def get_department(department_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        query = select(DepartmentModel).filter(DepartmentModel.id == department_id)
        result = await session.execute(query)
        department: DepartmentModel = result.scalars().unique().one_or_none()

        if department:
            return department
        else:
            raise HTTPException(
                detail="Department hasn't been found",
                status_code=status.HTTP_404_NOT_FOUND,
            )


# POST department
@router.post(
    "/", response_model=DepartmentSchemaCreate, status_code=status.HTTP_201_CREATED
)
async def post_departments(
    department: DepartmentSchemaCreate,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    new_department: DepartmentModel = DepartmentModel(**department.dict())
    department_name = new_department.name

    db.add(new_department)
    await db.commit()

    return JSONResponse({"detail": f"Department '{department_name}' has been created!"})


# PUT department
@router.put(
    "/{department_id}",
    response_model=DepartmentSchemaCreate,
    status_code=status.HTTP_200_OK,
)
async def get_department(
    department_id: int,
    department: DepartmentSchemaCreate,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    new_department: DepartmentModel = DepartmentModel(**department.dict())
    department_name = new_department.name

    async with db as session:
        query = select(DepartmentModel).filter(DepartmentModel.id == department_id)
        result = await session.execute(query)
        department_to_upd: DepartmentModel = result.scalars().unique().one_or_none()

        if department_to_upd:
            department_to_upd.name = department_name
            await session.commit()

            return department_to_upd

        else:
            raise HTTPException(
                detail="Department hasn't been found",
                status_code=status.HTTP_404_NOT_FOUND,
            )


# DELETE department
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    logged_user: UserModel = Depends(get_current_active_user),
):
    async with db as session:
        query = select(DepartmentModel).filter(DepartmentModel.id == department_id)
        result = await session.execute(query)
        department_del: DepartmentModel = result.scalars().unique().one_or_none()

        if department_del:
            department_name = department_del.name
            await session.delete(department_del)
            await session.commit()

            return JSONResponse(
                {"detail": f"Department '{department_name}' has been deleted!"}
            )
        else:
            raise HTTPException(
                detail="Department hasn't been found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
