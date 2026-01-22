from Services.CarService import CarService
from Services.UserService import UserService
from Services.AdminService import AdminService
from Services.BookingService import BookingService
from Services.PaymentService import PaymentService
from Services.CarService import CarService
from Services.AuthService import AuthService
from  Entities.Entity import User
from DB.SQLiteEngine import SQLiteEngine
from DB.MySQLEngine import MySQLEngine
import os
from Config import *
if __name__ == "__main__":
    print(os.getcwd())
    db = SQLiteEngine("./data/rental.db")
    # db=MySQLEngine("127.0.0.1","root","rootpassword","mydb")
    with open("init_sqlite.sql", "r") as f:
    # with open("init.sql", "r") as f:
        sql_contents = f.read()
        db.executescript(sql_contents)
        db.commit()    
    
    # user_service = UserService(db)
    # car_service = CarService(db)
    # booking_service = BookingService(db)
    # payment_service = PaymentService(db)
    # admin_service = AdminService(db)

    # # Register user
    # user_id = user_service.register_user("Mason", "mason@example.com", "securepass123")

    # # Add car (admin)
    # car_id = car_service.add_car({
    #     "make": "Toyota",
    #     "model": "Corolla",
    #     "year": 2023,
    #     "daily_rate": 189.99,
    #     "min_rent_days": 1,
    #     "max_rent_days": 30,
    #     "license_plate": "ABC123",
    #     "location_id": 1
    # })

    # # Customer books car
    # booking_id = booking_service.create_booking(
    #     user_id=user_id,
    #     car_id=car_id,
    #     start_date=datetime(2026, 2, 1),
    #     end_date=datetime(2026, 2, 5),
    #     pickup_location="Auckland Airport",
    #     drop_location="Auckland CBD"
    # )

    # # Calculate fee
    # fee = booking_service.calculate_rental_fee(booking_id)

    # # Admin approves
    # admin_service.approve_booking(booking_id)

    # # Pay
    # payment_service.process_payment(booking_id, fee.base_amount + fee.tax_amount)

    # Assume db is your DBEngine instance
    
    user_service = UserService(db);
    new_user = user_service.register_user(
        full_name="Mason Lee",
        email="mason@example.com",
        password="MySecurePass123!",
        phone="+64211234567"
    )
    print(f"New user ID: {new_user}")

    users = user_service.select()
    print("query all data",len(users))
    for _ in users:
        print(f"User: {_.full_name}, Email: {_.email}, Created: {_.create_time},password:{_.password}")

    auth_service = AuthService(db)
    user, token = auth_service.login("mason@example.com", "MySecurePass123!")
    setattr(auth_service, "current_user", user)
    print(f"Logged in user: {user.full_name}, Token: {token}")

    car_service = CarService(db)

    # Admin adds a car
    new_car_id = car_service.add_car({
        "make": "Toyota",
        "model": "Corolla Hybrid",
        "year": 2024,
        "mileage": 12000,
        "daily_rate": 89.99,
        "min_rent_days": 1,
        "max_rent_days": 60,
        "license_plate": "ABC-123",
        "color": "Silver",
        "location_id": 1,
        "category_id": 2
    })

    # Admin updates mileage and price
    car_service.update_car(new_car_id, {
        "mileage": 14500,
        "daily_rate": 94.50
    })

    # View available cars
    available = car_service.get_available_cars()
    for car in available:
        print(f"{car.make} {car.model} ({car.year}) - ${car.daily_rate}/day - Available: {car.is_available}")

    # Admin removes a car (soft delete)
    car_service.delete_car(new_car_id)
   
    db.close()