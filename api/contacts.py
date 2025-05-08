import logging

from typing import List
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from schemas import ContactModel, UpdateContact, ContactResponse
from services.contacts import ContactService


router = APIRouter(prefix="/contacts", tags=["contacts"])
logger = logging.getLogger("uvicorn.error")


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):

    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    name="Get contact by ID",
    description="Get contact by ID",
)
async def read_conact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    print(contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/search/", response_model=list[ContactResponse])
async def search_contacts(
    search_first_name: str = Query(default=""),
    search_last_name: str = Query(default=""),
    search_email: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts_by(
        search_first_name, search_last_name, search_email
    )

    return contacts


@router.get("/birthdays/", response_model=list[ContactResponse])
async def get_upcoming_birthdays(
    db: AsyncSession = Depends(get_db),
):
    cur_date = date.today()
    print(cur_date)

    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthdays(cur_date)

    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, body: UpdateContact, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return None
