from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ResourceModel(Base):
    __tablename__ = 'resource'

    id = Column(Integer(), primary_key=True)
    resource_name = Column(String(), nullable=True)
    resource_link = Column(String(), nullable=True)
    resource_method = Column(String(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True)
