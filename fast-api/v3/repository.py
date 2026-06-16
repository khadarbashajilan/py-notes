from sqlalchemy import select
from fastapi import HTTPException, status
from database import AsyncSessionLocal
from model import Credential, AddCred, UpdateCred
from typing import List


async def get_all() -> List[Credential]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Credential))
        return result.scalars().all()


async def get_credential(cred_id: int) -> Credential:
    async with AsyncSessionLocal() as session:
        query = select(Credential).where(Credential.id == cred_id)
        result = await session.execute(query)
        cred = result.scalar_one_or_none()

    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A credential for the id '{cred_id}' is not found.",
        )
    return cred


async def create_credential(payload: AddCred) -> Credential:
    async with AsyncSessionLocal() as session:
        existing = await session.execute(
            select(Credential).where(Credential.service_name == payload.service_name)
        )
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A credential for the service '{payload.service_name}' already exists.",
            )

        new_cred = Credential(**payload.model_dump())
        session.add(new_cred)
        await session.commit()
        await session.refresh(new_cred)
        return new_cred


async def partial_update(cred_id: int, payload: UpdateCred) -> Credential:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Credential).where(Credential.id == cred_id)
        )
        cred = result.scalar_one_or_none()

        if cred is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"A credential for the id '{cred_id}' is not found.",
            )

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(cred, key, value)

        await session.commit()
        await session.refresh(cred)
        return cred


async def full_update(cred_id: int, payload: AddCred) -> Credential:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Credential).where(Credential.id == cred_id)
        )
        cred = result.scalar_one_or_none()

        if cred is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"A credential for the id '{cred_id}' is not found.",
            )

        for key, value in payload.model_dump().items():
            setattr(cred, key, value)

        await session.commit()
        await session.refresh(cred)
        return cred
