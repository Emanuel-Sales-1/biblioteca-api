from app.database import Base
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    publication_year: Mapped[int]
    publisher: Mapped[str]

book_author = Table(
    "book_author",
    Base.metadata,
    Column("author_id", ForeignKey("author.id"), primary_key=True),
    Column("book_id", ForeignKey("book.id"), primary_key=True)
)