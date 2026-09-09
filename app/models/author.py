from app.database import Base
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional 

class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    birth_date: Mapped[Optional[date]]
    nationality: Mapped[str]