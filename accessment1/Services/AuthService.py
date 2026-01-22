# Services/AuthService.py
from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt  # pip install PyJWT
from Log import logger
from Entities.Entity import User
from Repositories.Repository import UserRepository


class AuthService:
    SECRET_KEY = "YOOBEE-PYTHON-ASSESSMENT"  # Use env var!
    ALGORITHM = "HS256"
    TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

    def __init__(self, db):
        self.db = db
        self.user_repo = UserRepository(db)


    def login(self, email: str, password: str) -> Tuple[User, str]:
        """Login user and return (user, jwt_token)"""
        users = self.user_repo.select({"email": email.lower()})
        if not users:
            raise ValueError("Invalid email or password")

        user = users[0]
        if user.status != 1:
            raise ValueError("Account is disabled")

        if user.password!=password:
            logger.warning(f"Failed login attempt for {email}")
            raise ValueError("Invalid email or password")

        # Generate JWT token
        payload = {
            "user_id": user.user_id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=self.TOKEN_EXPIRE_MINUTES)
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

        logger.info(f"User logged in: {email} (ID: {user.user_id})")
        setattr(self, "current_user", user)
        return user, token

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decode JWT token (used in middleware)"""
        try:
            return jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
        except jwt.PyJWTError as e:
            logger.warning(f"Invalid token: {e}")
            return None