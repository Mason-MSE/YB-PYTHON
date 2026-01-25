from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class BookingSchema(BaseModel):
    booking_id: Optional[int] = None
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pickup_location: Optional[str] = Field(None, max_length=100)
    drop_location: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None
    notes: Optional[str] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None,
            date: lambda v: v.strftime('%Y-%m-%d') if v else None,
            time: lambda v: v.strftime('%H:%M:%S') if v else None,
        }

class BookingCreateSchema(BaseModel):
    booking_id: int
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pickup_location: Optional[str] = Field(None, max_length=100)
    drop_location: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None
    notes: Optional[str] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None

    class Config:
        orm_mode = True

class BookingUpdateSchema(BaseModel):
    is_deleted: Optional[int] = None

    class Config:
        orm_mode = True
