from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from abc import ABC

class TimestampMixin:
    create_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    modify_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
