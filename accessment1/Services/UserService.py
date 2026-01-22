# services/auth_service.py
from typing import List, Optional, Dict, Any
from DB.DBEngine  import DBEngine
from datetime import datetime
from Log import logger
from Entities.Entity import User, UserProfile, DriverLicense
from Repositories.Repository import UserRepository, UserProfileRepository, DriverLicenseRepository


class UserService:
    def __init__(self, db: DBEngine):
        self.user_repo = UserRepository(db)
        self.profile_repo = UserProfileRepository(db)
        self.license_repo = DriverLicenseRepository(db)

    def register_user(self, full_name: str, email: str, password: str, phone: str = None) -> int:
        """Create a new user account"""
        existing = self.user_repo.select({"email": email})
        if existing:
            raise ValueError("Email already registered")

        user = User(
            full_name=full_name,
            email=email,
            password=password,  # In real system: hash the password!
            phone=phone,
            status=1,
            create_time=datetime.now()
        )
        user_id = self.user_repo.insert(user)
        logger.info(f"User registered: {email} (ID: {user_id})")
        return user_id

    def get_user_by_email(self, email: str) -> Optional[User]:
        users = self.user_repo.select({"email": email})
        return users[0] if users else None
    
    def select(self) -> List[User]:
        return self.user_repo.select()

    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]):
        profile = self.profile_repo.select({"user_id": user_id})
        if not profile:
            profile = UserProfile(user_id=user_id, **profile_data)
            self.profile_repo.insert(profile)
        else:
            profile = profile[0]
            for k, v in profile_data.items():
                setattr(profile, k, v)
            profile.modify_time = datetime.now()
            self.profile_repo.update_by_id(profile)