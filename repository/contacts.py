from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Contact
from schemas import ContactModel


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

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactModel
    ) -> Contact | None:
        contact = await self.get_tag_by_id(contact_id)
        if contact:
            contact.first_name = body.first_name
            contact.second_name = body.second_name
            contact.email = body.email
            contact.phone_number = body.phone_number
            contact.birthday = body.birthday
            contact.info = body.info
            await self.db.commit()
            await self.db.refresh(contact)
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
