from datetime import datetime
from Entities.BaseEntity import BaseEntity

from typing import Optional, Any
from datetime import datetime


from typing import Any

from Utils import _parse_date

# 1. User
class User(BaseEntity["User"]):
    __table__ = "user"
    __id_field__ = "user_id"
    __auto_increment__ = True

    def __init__(self, user_id=None, full_name=None, password=None, email=None, phone=None, 
                 status=None, create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.user_id = user_id
        self.full_name = full_name
        self.password = password
        self.email = email
        self.phone = phone
        self.status = status
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 2. User Profile
class UserProfile(BaseEntity["UserProfile"]):
    __table__ = "user_profile"
    __id_field__ = "profile_id"
    __auto_increment__ = True

    def __init__(self, profile_id=None, user_id=None, street=None, city=None, state_name=None,
                 zipcode=None, membership_type=None, driver_license_id=None, avatar_url=None,
                 date_of_birth=None, nationality=None, emergency_contact_name=None,
                 emergency_contact_phone=None, preferred_language=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.profile_id = profile_id
        self.user_id = user_id
        self.street = street
        self.city = city
        self.state_name = state_name
        self.zipcode = zipcode
        self.membership_type = membership_type
        self.driver_license_id = driver_license_id
        self.avatar_url = avatar_url
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.preferred_language = preferred_language
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 3. Driver License
class DriverLicense(BaseEntity["DriverLicense"]):
    __table__ = "driver_license"
    __id_field__ = "driver_license_id"
    __auto_increment__ = True

    def __init__(self, driver_license_id=None, user_id=None, license_pic=None, expire_date=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.driver_license_id = driver_license_id
        self.user_id = user_id
        self.license_pic = license_pic
        self.expire_date = expire_date
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 4. Role
class Role(BaseEntity["Role"]):
    __table__ = "role"
    __id_field__ = "role_id"
    __auto_increment__ = True

    def __init__(self, role_id=None, role_name=None, create_time=None, modify_time=None,
                 is_deleted=None, **kwargs):
        self.role_id = role_id
        self.role_name = role_name
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 5. Resource
class Resource(BaseEntity["Resource"]):
    __table__ = "resource"
    __id_field__ = "resource_id"
    __auto_increment__ = True

    def __init__(self, resource_id=None, resource_name=None, resource_link=None,
                 resource_method=None, create_time=None, modify_time=None,
                 is_deleted=None, **kwargs):
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_link = resource_link
        self.resource_method = resource_method
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 6. User Role (junction table)
class UserRole(BaseEntity["UserRole"]):
    __table__ = "user_role"
    __id_field__ = "user_role_id"
    __auto_increment__ = True

    def __init__(self, user_role_id=None, user_id=None, role_id=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.user_role_id = user_role_id
        self.user_id = user_id
        self.role_id = role_id
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 7. Role Resource (junction table)
class RoleResource(BaseEntity["RoleResource"]):
    __table__ = "role_resource"
    __id_field__ = "role_resource_id"
    __auto_increment__ = True

    def __init__(self, role_resource_id=None, role_id=None, resource_id=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.role_resource_id = role_resource_id
        self.role_id = role_id
        self.resource_id = resource_id
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 8. Car Category
class CarCategory(BaseEntity["CarCategory"]):
    __table__ = "car_category"
    __id_field__ = "car_category_id"
    __auto_increment__ = True

    def __init__(self, car_category_id=None, category_name=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.car_category_id = car_category_id
        self.category_name = category_name
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 9. Location
class Location(BaseEntity["Location"]):
    __table__ = "location"
    __id_field__ = "location_id"
    __auto_increment__ = True

    def __init__(self, location_id=None, location_name=None, street=None, zipcode=None,
                 city=None, state_name=None, create_time=None, modify_time=None,
                 is_deleted=None, **kwargs):
        self.location_id = location_id
        self.location_name = location_name
        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.state_name = state_name
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 10. Car
class Car(BaseEntity["Car"]):
    __table__ = "car"
    __id_field__ = "car_id"
    __auto_increment__ = True

    def __init__(self, car_id=None, make=None, model=None, year=None, mileage=None,
                 is_available=None, min_rent_days=None, max_rent_days=None,
                 license_plate=None, color=None, daily_rate=None, location_id=None,
                 category_id=None, create_time=None, modify_time=None,
                 is_deleted=None, **kwargs):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.is_available = is_available
        self.min_rent_days = min_rent_days
        self.max_rent_days = max_rent_days
        self.license_plate = license_plate
        self.color = color
        self.daily_rate = daily_rate
        self.location_id = location_id
        self.category_id = category_id
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 11. Booking
class Booking(BaseEntity["Booking"]):
    __table__ = "booking"
    __id_field__ = "booking_id"
    __auto_increment__ = True

    def __init__(self, booking_id=None, user_id=None, car_id=None, start_date:Optional[datetime]=None,
                 end_date=None, pickup_location=None, drop_location=None, status=None,
                 notes=None, color=None, create_time:Optional[datetime]=None, modify_time:Optional[datetime]=None,
                 is_deleted=None, **kwargs):
        self.booking_id = booking_id
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = _parse_date(start_date)
        self.end_date = _parse_date(end_date)
        self.pickup_location = pickup_location
        self.drop_location = drop_location
        self.status = status
        self.notes = notes
        self.color = color
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 12. Rent Fee
class RentFee(BaseEntity["RentFee"]):
    __table__ = "rent_fee"
    __id_field__ = "rent_fee_id"
    __auto_increment__ = True

    def __init__(self, rent_fee_id=None, booking_id=None, base_amount=None,
                 insurance_amount=None, late_fee=None, discount_amount=None,
                 tax_amount=None, payment_status=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.rent_fee_id = rent_fee_id
        self.booking_id = booking_id
        self.base_amount = base_amount
        self.insurance_amount = insurance_amount
        self.late_fee = late_fee
        self.discount_amount = discount_amount
        self.tax_amount = tax_amount
        self.payment_status = payment_status
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)


# 13. Payment
class Payment(BaseEntity["Payment"]):
    __table__ = "payment"
    __id_field__ = "payment_id"
    __auto_increment__ = True

    def __init__(self, payment_id=None, booking_id=None, rent_fee_id=None,
                 payment_amount=None, payment_date=None, payment_method=None,
                 transaction_id=None, payment_status=None, reference_number=None,
                 payer_name=None, notes=None,
                 create_time=None, modify_time=None, is_deleted=None, **kwargs):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.rent_fee_id = rent_fee_id
        self.payment_amount = payment_amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.transaction_id = transaction_id
        self.payment_status = payment_status
        self.reference_number = reference_number
        self.payer_name = payer_name
        self.notes = notes
        self.create_time = create_time
        self.modify_time = modify_time
        self.is_deleted = is_deleted
        super().__init__(**kwargs)