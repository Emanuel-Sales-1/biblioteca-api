from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    publication_year: Mapped[int]
    publisher: Mapped[str]