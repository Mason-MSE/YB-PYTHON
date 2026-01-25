from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.booking import BookingSchema,BookingCreateSchema,BookingUpdateSchema
from cruds.booking import get, get_all, create, update, delete

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
    return create(db, item_in)

@router.put('/{booking_id}', response_model=BookingSchema)
def update_item(booking_id, item_in: BookingUpdateSchema, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    return update(db, db_obj, item_in)

@router.delete('/{booking_id}')
def delete_item(booking_id, db: Session = Depends(get_db)):
    db_obj = get(db, booking_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail='Item not found')
    delete(db, db_obj)
    return {'ok': True}
