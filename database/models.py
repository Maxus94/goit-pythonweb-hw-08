from datetime import date

from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import DateTime

from conf import constants


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contactes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(
        String(constants.NAME_MAX_LEN), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(constants.NAME_MAX_LEN), nullable=False
    )
    email: Mapped[str] = mapped_column(String(constants.EMAIL_MAX_LEN), nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String(constants.PHONE_MAX_LEN), nullable=False
    )
    birthday: Mapped[date] = mapped_column(DateTime, nullable=False)
    info: Mapped[str] = mapped_column(String(constants.INFO_MAX_LEN), nullable=True)

    def __repr__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.phone_number} {self.birthday}"
