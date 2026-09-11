from app.database import Base
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class Loan(Base):
    __tablename__ = "loan"

    id: Mapped[int] = mapped_column(primary_key=True)
    copy_id: Mapped[int] = mapped_column(ForeignKey("copy.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    loan_date: Mapped[date]
    due_date: Mapped[date]
    return_date: Mapped[Optional[date]]
    