from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from conf import constants, messages


class ContactModel(BaseModel):
    first_name: str = Field(
        max_length=constants.NAME_MAX_LEN,
        description=messages.contact_schema_first_name,
    )
    last_name: str = Field(
        max_length=constants.NAME_MAX_LEN, description=messages.contact_schema_last_name
    )
    email: str = Field(
        max_length=constants.EMAIL_MAX_LEN, description=messages.contact_schema_email
    )
    phone_number: str = Field(
        max_length=constants.PHONE_MAX_LEN,
        description=messages.contact_schema_phone_number,
    )
    birthday: date = Field(description=messages.contact_schema_birthday)
    info: Optional[str] = Field(
        max_length=constants.INFO_MAX_LEN, description=messages.contact_schema_info
    )


class CreateContact(ContactModel):
    pass


class UpdateContact(ContactModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    info: Optional[str] = None


class ContactResponse(ContactModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
