# services/booking_service.py
from datetime import datetime
from typing import List, Optional, Dict, Any
from DB.DBEngine  import DBEngine
from Log import logger  
from typing import Optional
from Entities.Entity import Booking, Car, RentFee
from Repositories.Repository import BookingRepository, CarRepository, RentFeeRepository
from Services.CarService import CarService


class BookingService:
    def __init__(self, db: DBEngine):
        self.booking_repo = BookingRepository(db)
        self.car_repo = CarRepository(db)
        self.rent_fee_repo = RentFeeRepository(db)

    def create_booking(self, user_id: int, car_id: int,
                       start_date: datetime, end_date: datetime,
                       pickup_location: str, drop_location: str) -> int:
        """Customer: Create a booking request"""
        car = self.car_repo.select_by_id(car_id)
        if not car or not car.is_available:
            raise ValueError("Car not available")

       # Convert strings to datetime if needed
        if isinstance(start_date, str):
            start = datetime.fromisoformat(start_date)
        else:
            start = start_date

        if isinstance(end_date, str):
            end = datetime.fromisoformat(end_date)
        else:
            end = end_date

        days = (end - start).days
        if days < car.min_rent_days or days > car.max_rent_days:
            raise ValueError(f"Rental period must be between {car.min_rent_days} and {car.max_rent_days} days")

        booking = Booking(
            user_id=user_id,
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
            pickup_location=pickup_location,
            drop_location=drop_location,
            status="pending",
            create_time=datetime.now()
        )
        booking_id = self.booking_repo.insert(booking)

        # Mark car as unavailable (simple approach — real system would use date-range check)
        car.is_available = False
        car.modify_time = datetime.now()
        self.car_repo.update_by_id(car)

        logger.info(f"Booking created: ID {booking_id} for user {user_id}")
        return booking_id

    def calculate_rental_fee(self, booking_id: int) -> RentFee:
        """Calculate and store rental fee for a booking"""
        booking = self.booking_repo.select_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        car = self.car_repo.select_by_id(booking.car_id)
        days = (booking.end_date - booking.start_date).days

        base_amount = days * car.daily_rate
        # You can add insurance, discount, tax logic here
        insurance_amount = 0.0  # placeholder
        late_fee = 0.0
        discount_amount = 0.0
        tax_amount = base_amount * 0.15  # example 15% tax
        total = base_amount + insurance_amount + late_fee + tax_amount - discount_amount

        fee = RentFee(
            booking_id=booking_id,
            base_amount=base_amount,
            insurance_amount=insurance_amount,
            late_fee=late_fee,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            payment_status=0,  # pending
            create_time=datetime.now()
        )
        fee_id = self.rent_fee_repo.insert(fee)
        logger.info(f"Fee calculated for booking {booking_id}: ${total:.2f}")
        return fee