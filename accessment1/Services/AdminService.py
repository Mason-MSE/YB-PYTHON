from datetime import datetime
from typing import List, Optional, Dict, Any
from DB.DBEngine  import DBEngine
from Log import logger  
from typing import Optional
from Entities.Entity import Booking, Car, RentFee
from Repositories.Repository import CarRepository,BookingRepository
from Services.CarService import CarService

class AdminService:
    def __init__(self, db: DBEngine):
        self.car_service = CarService(db)
        self.booking_repo = BookingRepository(db)

    def approve_booking(self, booking_id: int):
        booking = self.booking_repo.select_by_id(booking_id)
        if not booking or booking.status != "pending":
            raise ValueError("Invalid booking status")
        booking.status = "confirmed"
        booking.modify_time = datetime.now()
        self.booking_repo.update_by_id(booking)
        logger.info(f"Booking {booking_id} approved")

    def reject_booking(self, booking_id: int):
        booking = self.booking_repo.select_by_id(booking_id)
        if not booking or booking.status != "pending":
            raise ValueError("Invalid booking status")
        booking.status = "rejected"
        booking.modify_time = datetime.now()
        self.booking_repo.update_by_id(booking)

        # Return car availability
        car = self.car_service.car_repo.select_by_id(booking.car_id)
        if car:
            car.is_available = True
            car.modify_time = datetime.now()
            self.car_service.car_repo.update_by_id(car)
        logger.info(f"Booking {booking_id} rejected")