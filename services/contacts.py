import logging

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from repository.contacts import ContactRepository
from schemas import ContactModel

logger = logging.getLogger("uvicorn.error")


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel):
        return await self.repository.create_contact(body)

    async def get_contacts(self, skip: int, limit: int):
        return await self.repository.get_contacts(skip, limit)

    async def get_contacts_by(
        self, search_first_name: Query, search_last_name: Query, search_email: Query
    ):

        return await self.repository.get_contacts_by(
            search_first_name, search_last_name, search_email
        )

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def get_upcoming_birthdays(self, cur_date):
        return await self.repository.get_upcoming_birthdays(cur_date)

    async def update_contact(self, contact_id: int, body: ContactModel):
        return await self.repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.repository.remove_contact(contact_id)
