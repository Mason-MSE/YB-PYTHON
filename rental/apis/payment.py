from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.booking import BookingUpdateSchema
from schemas.payment import PaymentSchema,PaymentCreateSchema,PaymentUpdateSchema
from cruds.payment import get, get_all, create, get_by_booking_id, update, delete
import cruds.booking as booking_crud


router = APIRouter(prefix='/payment', tags=['payment'])

@router.get('/', response_model=List[PaymentSchema])
def read_all(db: Session = Depends(get_db)):
    return get_all(db)

@router.get('/{payment_id}', response_model=PaymentSchema)
def read_item(payment_id, db: Session = Depends(get_db)):
    db_obj = get(db, payment_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_obj

@router.post('/', response_model=PaymentSchema)
def create_item(item_in: PaymentCreateSchema, db: Session = Depends(get_db)):
    payment_model = get_by_booking_id(db,item_in.booking_id)
    if payment_model:
        raise HTTPException(status_code=400, detail='Payment already payed')
    payment=create(db, item_in)
    bookingid=item_in.booking_id
    bookingmodel=booking_crud.get(db,bookingid) 
    if not bookingmodel:
        raise HTTPException(status_code=400, detail='Associated booking does not exist')
    booking_crud.update(db,bookingmodel,BookingUpdateSchema(status=3))
    return payment

@router.put('/{payment_id}', response_model=PaymentSchema)
def update_item(payment_id, item_in: PaymentUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, payment_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{payment_id}')
def delete_item(payment_id, db: Session = Depends(get_db)):
    db_obj = get(db, payment_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
