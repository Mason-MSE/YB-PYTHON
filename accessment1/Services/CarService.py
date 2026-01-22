# services/car_service.py
from datetime import datetime
from typing import List, Optional, Dict, Any
from DB.DBEngine  import DBEngine
from Log import logger
from Entities.Entity import Car, CarCategory
from Repositories.Repository import CarRepository,CarCategoryRepository,LocationRepository
from PermissionDenied import require_role


class CarService:
    def __init__(self, db: DBEngine):
        self.car_repo = CarRepository(db)
        self.category_repo = CarCategoryRepository(db)
        self.location_repo = LocationRepository(db)

    def update_car_availability(self, car_id: int, available: bool):
        car = self.car_repo.select_by_id(car_id)
        if not car:
            raise ValueError("Car not found")
        car.is_available = available
        car.modify_time = datetime.now()
        self.car_repo.update_by_id(car)
    
    @require_role("admin")   # ← only admins can manage cars
    def add_car(self, car_data: Dict[str, Any]) -> int:
        """
        Admin: Add a new car to the system
        """
        required_fields = ["make", "model", "year", "daily_rate"]
        for field in required_fields:
            if field not in car_data or car_data[field] is None:
                raise ValueError(f"Missing required field: {field}")

        car = Car(
            make=car_data["make"],
            model=car_data["model"],
            year=car_data["year"],
            mileage=car_data.get("mileage", 0),
            is_available=car_data.get("is_available", True),
            min_rent_days=car_data.get("min_rent_days", 1),
            max_rent_days=car_data.get("max_rent_days", 30),
            license_plate=car_data.get("license_plate"),
            color=car_data.get("color"),
            daily_rate=float(car_data["daily_rate"]),
            location_id=car_data.get("location_id"),
            category_id=car_data.get("category_id"),
            create_time=datetime.now(),
            modify_time=datetime.now()
        )

        car_id = self.car_repo.insert(car)
        logger.info(f"Admin added new car: {car.make} {car.model} (ID: {car_id})")
        return car_id

    @require_role("admin")
    def update_car(self, car_id: int, update_data: Dict[str, Any]) -> bool:
        """
        Admin: Update existing car details
        """
        car = self.car_repo.select_by_id(car_id)
        if not car:
            raise ValueError(f"Car with ID {car_id} not found")

        # Only update provided fields
        for key, value in update_data.items():
            if hasattr(car, key) and value is not None:
                setattr(car, key, value)

        car.modify_time = datetime.now()
        self.car_repo.update_by_id(car)
        logger.info(f"Admin updated car ID {car_id}")
        return True

    @require_role("admin")
    def delete_car(self, car_id: int, hard_delete: bool = False) -> bool:
        """
        Admin: Soft delete or hard delete a car
        """
        car = self.car_repo.select_by_id(car_id)
        if not car:
            raise ValueError(f"Car with ID {car_id} not found")

        if hard_delete:
            self.car_repo.hard_delete_by_id(car_id)
            logger.warning(f"Admin hard-deleted car ID {car_id}")
        else:
            self.car_repo.soft_delete_by_id(car_id)
            logger.info(f"Admin soft-deleted car ID {car_id}")

        return True

    def get_available_cars(self, location_id: Optional[int] = None) -> List[Car]:
        """
        Customer/Admin: View currently available cars
        (No role restriction – everyone can see available cars)
        """
        conditions = {"is_available": True, "is_deleted": 0}
        if location_id is not None:
            conditions["location_id"] = location_id

        cars = self.car_repo.select(conditions=conditions)
        logger.debug(f"Retrieved {len(cars)} available cars")
        return cars

    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """Get single car details (used in booking, admin view, etc.)"""
        return self.car_repo.select_by_id(car_id)