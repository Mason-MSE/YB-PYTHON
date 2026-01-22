# services/payment_service.py
from datetime import datetime
from typing import Optional
from DB.DBEngine  import DBEngine
from Entities.Entity import Payment, RentFee
from Log import logger
from Repositories.Repository import PaymentRepository, RentFeeRepository,BookingRepository


class PaymentService:
    def __init__(self, db: DBEngine):
        self.payment_repo = PaymentRepository(db)
        self.rent_fee_repo = RentFeeRepository(db)
        self.booking_repo = BookingRepository(db)

    def process_payment(self, booking_id: int, amount: float,
                        method: str = "credit_card", transaction_id: str = None) -> int:
        """Record a payment (partial or full)"""
        booking = self.booking_repo.select_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        payment = Payment(
            booking_id=booking_id,
            payment_amount=amount,
            payment_date=datetime.now(),
            payment_method=method,
            transaction_id=transaction_id,
            payment_status=1,  # completed
            create_time=datetime.now()
        )
        payment_id = self.payment_repo.insert(payment)

        # Optional: update rent_fee payment status if fully paid
        # (requires summing payments vs total due)

        logger.info(f"Payment recorded: ${amount:.2f} for booking {booking_id}")
        return payment_id