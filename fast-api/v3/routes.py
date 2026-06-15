from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schema import AddCred, UpdateCred, CredResponse
from model import Credential
from typing import List

router = APIRouter(prefix="/credentials", tags=["Credentials"])

@router.get("/", response_model=List[CredResponse])
async def get_all(db:AsyncSession = Depends(get_db)):
    statement = select(Credential)
    result = await db.execute(statement)
    credentials = result.scalars().all()
    return credentials

@router.get("/{id}", response_model=CredResponse)
async def get_credential(id:int, db:AsyncSession = Depends(get_db)):
    query = select(Credential).where(Credential.id==id)
    query_result = await db.execute(query)
    found_cred = query_result.scalar_one_or_none()
    if found_cred is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A credential for the id '{id}' is not found."
        )
    return found_cred
    

@router.post("/", response_model=CredResponse)
async def create_credential(payload:AddCred, db:AsyncSession = Depends(get_db)):
    #check for duplis before adding to db
    duplicate_query = select(Credential).where(Credential.service_name==payload.service_name)
    query_result = await db.execute(duplicate_query)
    existing_service = query_result.scalar_one_or_none()

    if existing_service is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A credential for the service '{payload.service_name}' already exists."
        )

    #converting pydantic validation -> Python dict
    data_dict = payload.model_dump()
    new_cred = Credential(**data_dict)
    #placing to session internals
    db.add(new_cred)
    #Asynchronously commit the transaction
    await db.commit()
    #Refresh the object from db
    await db.refresh(new_cred)
    return new_cred


@router.put("/{id}", response_model=CredResponse)
async def update_credential(id:int, payload:UpdateCred, db:AsyncSession = Depends(get_db)):
    #check is the credential available with this id
    check_query = select(Credential).where(Credential.id==id)
    query_result = await db.execute(check_query)
    found_cred = query_result.scalar_one_or_none()

    if found_cred is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A credential for the id '{id}' is not found."
        )

   #Extracts only the field which were provided by user 
   update_data = payload.model_dump(exclude_unset=True)

   #Apply update dynamically
   for key, value in update_data.items():
       setattr(found_cred, key, value)

    #db.add(found_cred) -> why? object is tracked by session no need to add again, its already done by sqlalchemy

    await db.commit()
    await db.refresh(found_cred)

    return found_cred

