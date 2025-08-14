from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from database.database import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

