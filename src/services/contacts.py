from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactModel


class ContactService:

    def __init__(self, db: AsyncSession) -> None:
        self.repository = ContactRepository(db)

    async def get_contacts(self, skip: int, limit: int):
        return await self.repository.get_contacts(skip, limit)

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def create_contact(self, body: ContactModel):
        return await self.repository.create_contact(body)

    async def update_contact(self, contact_id: int, body: ContactModel):
        return await self.repository.update_contact(contact_id, body)

    async def delete_contact(self, contact_id):
        return await self.repository.remove_contact(contact_id)

    async def search_contact(self, first_name: str = None, second_name: str = None, email: str = None):
        return await self.repository.search_contacts(first_name, second_name, email)

    async def get_upcoming_birthdays(self):
        return await self.repository.get_upcoming_birthdays()
