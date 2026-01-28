from pydantic import BaseModel,Field, constr
from datetime import datetime, date, time
from typing import Optional

class DriverLicenseSchema(BaseModel):
    driver_license_id: Optional[int] = None
    user_id: Optional[int] = None
    license_pic: Optional[str] = Field(None, max_length=255)
    driver_license: Optional[str] = Field(None, max_length=50)
    expire_date: Optional[date] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None
    drive_number: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None,
            date: lambda v: v.strftime('%Y-%m-%d') if v else None,
            time: lambda v: v.strftime('%H:%M:%S') if v else None,
        }

class DriverLicenseCreateSchema(BaseModel):
    driver_license_id: int
    user_id: Optional[int] = None
    license_pic: Optional[str] = Field(None, max_length=255)
    driver_license: Optional[str] = Field(None, max_length=50)
    expire_date: Optional[date] = None
    create_time: Optional[datetime] = None
    modify_time: Optional[datetime] = None
    is_deleted: Optional[int] = None
    drive_number: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True

class DriverLicenseUpdateSchema(BaseModel):
    drive_number: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True
