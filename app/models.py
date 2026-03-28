from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Note(Base):
    __tablename__ = "notes"

    # ID: auto-incrementing primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # title: string, max length 255, cannot be empty
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # content: text, cannot be empty
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # created_at: automatically set by the database (func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # updated_at: updated by the database on each row modification
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        onupdate=func.now()
    )