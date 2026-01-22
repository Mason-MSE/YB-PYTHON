from Repositories.BaseRepository import Repository
from Entities.Entity import *

# ---------------- Student Repository ----------------
class UserRepository(Repository[User]):
    def __init__(self, db):
        super().__init__(db, User.__table__, User)


class UserProfileRepository(Repository[UserProfile]):
    def __init__(self, db):
        super().__init__(db, UserProfile.__table__, UserProfile)


class DriverLicenseRepository(Repository[DriverLicense]):
    def __init__(self, db):
        super().__init__(db, DriverLicense.__table__, DriverLicense)


class RoleRepository(Repository[Role]):
    def __init__(self, db):
        super().__init__(db, Role.__table__, Role)


class ResourceRepository(Repository[Resource]):
    def __init__(self, db):
        super().__init__(db, Resource.__table__, Resource)


class UserRoleRepository(Repository[UserRole]):
    def __init__(self, db):
        super().__init__(db, UserRole.__table__, UserRole)


class RoleResourceRepository(Repository[RoleResource]):
    def __init__(self, db):
        super().__init__(db, RoleResource.__table__, RoleResource)


class CarCategoryRepository(Repository[CarCategory]):
    def __init__(self, db):
        super().__init__(db, CarCategory.__table__, CarCategory)


class LocationRepository(Repository[Location]):
    def __init__(self, db):
        super().__init__(db, Location.__table__, Location)


class CarRepository(Repository[Car]):
    def __init__(self, db):
        super().__init__(db, Car.__table__, Car)


class BookingRepository(Repository[Booking]):
    def __init__(self, db):
        super().__init__(db, Booking.__table__, Booking)


class RentFeeRepository(Repository[RentFee]):
    def __init__(self, db):
        super().__init__(db, RentFee.__table__, RentFee)


class PaymentRepository(Repository[Payment]):
    def __init__(self, db):
        super().__init__(db, Payment.__table__, Payment)