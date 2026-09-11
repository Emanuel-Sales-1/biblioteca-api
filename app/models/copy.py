from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Copy(Base):
    __tablename__ = "copy"

    id: Mapped[int] = mapped_column(primary_key=True)
    identification_code: Mapped[int] = mapped_column(unique=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
