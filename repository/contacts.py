from typing import List
from fastapi import Query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Contact
from schemas import ContactModel, UpdateContact


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def get_contacts_by(
        self, search_first_name: str, search_last_name: str, search_email: str
    ) -> List[Contact] | None:
        stmt = select(Contact).where(
            Contact.first_name.ilike(f"%{search_first_name}%"),
            Contact.last_name.ilike(f"%{search_last_name}%"),
            Contact.email.ilike(f"%{search_email}%"),
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_upcoming_birthdays(self, cur_date) -> List[Contact]:
        # stmt = select(Contact).filter(int((Contact.birthday - cur_date).days) <= 7)
        stmt = select(Contact)
        contacts = await self.db.execute(stmt)

        for contact in contacts:
            print(contact.email)

        return contacts.scalars().all()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: UpdateContact
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)

        update_data = body.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(contact, key, val)
        return contact

    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_contacts_by_ids(self, contact_ids: list[int]) -> list[Contact]:
        stmt = select(Contact).where(Contact.id.in_(contact_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()
