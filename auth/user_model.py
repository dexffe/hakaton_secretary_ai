from sqlalchemy import Integer, String, Boolean, MetaData
from sqlalchemy.orm import mapped_column, Mapped

from db.db import Base

metadata = MetaData()


class User(Base):
    __tablename__ = "user"
    metadata = metadata
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )


