from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserRoleModel(Base):
    __tablename__ = 'user_role'

    user_id = Column(Integer(), primary_key=True)
    role_id = Column(Integer(), primary_key=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True)
