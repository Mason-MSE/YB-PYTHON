from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from core.dependencies import require_permission
from schemas.rent_fee import RentFeeCreateSchema, RentFeeUpdateSchema
from schemas.car import CarUpdateSchema
from schemas.booking import BookingApprovalSchema, BookingReturnCarSchema, BookingSchema,BookingCreateSchema,BookingUpdateSchema
from cruds.booking import get, get_all, create, update, delete
import cruds.car as car_crud
import cruds.rent_fee as rent_fee_crud


router = APIRouter(prefix='/booking', tags=['booking'])

@router.get('/', response_model=List[BookingSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{booking_id}', response_model=BookingSchema)
def read_item(booking_id, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=BookingSchema)
def create_item(item_in: BookingCreateSchema, db: Session = Depends(get_db)):
    car=car_crud.get(db, item_in.car_id)  # Ensure the car exists
    if not car:
        raise HTTPException(status_code=400, detail='Car does not exist')
    if car.is_available != 1: # Assuming 1 means available            
        raise HTTPException(status_code=400, detail='Car is not available for booking')
    bookingmodel=create(db, item_in)

    base_amount=car.daily_rate*(bookingmodel.end_time - bookingmodel.start_time).total_seconds()/3600,
    rent_fee_crud.create(db, RentFeeCreateSchema(bookingmodel.booking_id,
                                                base_amount=base_amount,
                                                insurance_amount=10.0,
                                                tax_amount=base_amount*0.01,
                                                late_fee=0.0,
                                                discount_amount=0.0
                                                ) ) # Create associated rent fee record)
    return bookingmodel

@router.put('/{booking_id}', response_model=BookingSchema)
def update_item(booking_id, item_in: BookingUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    car=car_crud.get(db, db_obj.car_id) 
    if not car:
        raise HTTPException(status_code=400, detail='Car does not exist')
    if car.is_available != 1: # Assuming 1 means available            
        raise HTTPException(status_code=400, detail='Car is not available for booking')
    
    print("Updating booking:", db_obj, "with data:", item_in)
    bookingmodel = update(db, db_obj, item_in)
    print("Updated booking:", bookingmodel)
    
    hours = Decimal(
    (bookingmodel.end_date - bookingmodel.start_date).total_seconds()) / Decimal("3600")
    hourly_rate = Decimal(car.daily_rate) / Decimal("24")
    base_amount = (hourly_rate * hours).quantize(
        Decimal("0.00"),
        rounding=ROUND_HALF_UP
    )
    print("hours:", hours, "hours_rate:", hourly_rate, "Calculated base amount:", base_amount)
    rent_fee = rent_fee_crud.get_by_booking_id(db, bookingmodel.booking_id)
    if  not rent_fee:
        rent_fee_crud.create(db, RentFeeCreateSchema(
                                                booking_id=bookingmodel.booking_id,
                                                base_amount=base_amount,
                                                insurance_amount=10.0,
                                                tax_amount=round(float(base_amount) * 0.01, 2),
                                                late_fee=0.0,
                                                discount_amount=0.0,
                                                total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2)   
                                                )) # Create associated rent fee record)
    else:
        rent_fee_crud.update(db, rent_fee,RentFeeUpdateSchema(
                                                    booking_id=bookingmodel.booking_id,
                                                    base_amount=base_amount,
                                                    insurance_amount=10.0,
                                                    tax_amount=round(float(base_amount) * 0.01, 2),
                                                    late_fee=0.0,
                                                    discount_amount=0.0,
                                                    total_amount=round(float(base_amount) + 10.0 + round(float(base_amount) * 0.01, 2),2) 
                                                    ) ) # update associated rent fee record)

    return bookingmodel

@router.delete('/{booking_id}')
def delete_item(booking_id, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}

@router.put('/approval/{booking_id}')
def approval(booking_id,item_in: BookingApprovalSchema, db: Session = Depends(get_db),user=Depends(require_permission())):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    if db_obj.status != 0:
        raise HTTPException(status_code=400, detail='Booking has already been processed')
    if item_in.status==1:
        car_model = car_crud.get(db, db_obj.car_id)  # Mark car as available    
        if not car_model:
            raise HTTPException(status_code=404, detail='Item not found')
        car_crud.update(db, car_model, CarUpdateSchema(is_available=0))  # Mark car as not available
    return update(db, db_obj, item_in)

@router.put('/return/{booking_id}')
def return_car( item_in: BookingReturnCarSchema,db: Session = Depends(get_db)):
    db_obj = get(db, item_in.booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    car_model = car_crud.get(db, db_obj.car_id)  # Mark car as available    
    if not car_model:
        raise HTTPException(status_code=404, detail='Item not found')
    car_crud.update(db, car_model, CarUpdateSchema(is_available=1,location_id=item_in.drop_location))  # Mark car as available
    current_time=datetime.now()
    if current_time > db_obj.end_date:
        # Calculate late fee
        late_hours = Decimal(
            (current_time - db_obj.end_date).total_seconds()) / Decimal("3600")
        hourly_rate = Decimal(car_model.daily_rate) / Decimal("24")
        late_fee = (hourly_rate * late_hours).quantize(
            Decimal("0.00"),
            rounding=ROUND_HALF_UP
        )
        rent_fee = rent_fee_crud.get_by_booking_id(db, db_obj.booking_id)
        if rent_fee:
            rent_fee_crud.update(db, rent_fee, RentFeeUpdateSchema(
                late_fee=late_fee,
                total_amount=rent_fee.total_amount + float(late_fee)
            ))

    bookingmodel=update(db, db_obj, BookingUpdateSchema(status=2, drop_location=item_in.drop_location, drop_time=current_time))
    return bookingmodel