from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    completed: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False)
