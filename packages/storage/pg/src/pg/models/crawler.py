from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class Crawler(Base):
    __tablename__ = "crawlers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Crawler(id={self.id}, url={self.url}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})>"
