from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BookingModel(Base):
    __tablename__ = 'booking'

    booking_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=True)
    car_id = Column(Integer(), nullable=True)
    start_date = Column(DateTime(), nullable=True)
    end_date = Column(DateTime(), nullable=True)
    pickup_location = Column(String(), nullable=True)
    drop_location = Column(String(), nullable=True)
    status = Column(String(), nullable=True)
    notes = Column(String(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True)
