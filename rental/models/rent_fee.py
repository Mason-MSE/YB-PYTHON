from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RentFeeModel(Base):
    __tablename__ = 'rent_fee'

    rent_fee_id = Column(Integer(), primary_key=True)
    booking_id = Column(Integer(), nullable=True)
    base_amount = Column(Float(), nullable=True)
    insurance_amount = Column(Float(), nullable=True)
    late_fee = Column(Float(), nullable=True)
    discount_amount = Column(Float(), nullable=True)
    tax_amount = Column(Float(), nullable=True)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    is_deleted = Column(Integer(), nullable=True)
