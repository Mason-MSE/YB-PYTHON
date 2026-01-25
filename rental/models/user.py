from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

Base = declarative_base()

class UserModel(Base,):
    __tablename__ = 'user'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    create_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    modify_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    is_deleted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __mapper_args__ = {
        "eager_defaults": True
    }

@event.listens_for(UserModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):  
    target.modify_time = datetime.now() 

@event.listens_for(UserModel, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target):  
    target.create_time = datetime.now() 
    target.modify_time = datetime.now()
