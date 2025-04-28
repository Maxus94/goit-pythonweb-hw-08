from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contactes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    birthday: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    info: Mapped[str] = mapped_column(String(500), nullable=True)
