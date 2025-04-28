from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone_number: str = Field(max_length=15)
    birthday: datetime = Field()
    info: Optional[str] = Field(max_length=500)


class CreateContact(ContactModel):
    pass


class UpdateContact(ContactModel):
    first_name: Optional[str] = None
    last_name_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None
    optional_data: Optional[str] = None


class ContactResponse(ContactModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
