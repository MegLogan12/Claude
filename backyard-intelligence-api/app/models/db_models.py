"""Database models for persistence and analytics."""

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PropertyAnalysisRecord(Base):
    __tablename__ = "property_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(500), index=True)
    lead_quality: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
