from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base

class Manager(Base):
    __tablename__ = "managers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True)
