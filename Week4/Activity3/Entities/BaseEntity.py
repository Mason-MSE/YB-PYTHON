from datetime import datetime
from typing import Any, Dict, TypeVar, Generic

T=TypeVar("T")
class BaseEntity(Generic[T]):
    #Base entity class containing audit fields and soft delete flag.
    def __init__(self, create_time=None, modify_time=None, is_deleted=0):
        self.create_time = create_time or datetime.now()
        self.modify_time = modify_time or datetime.now()
        self.is_deleted = is_deleted

    def __str__(self) -> str:
        # Generic human-readable string representation.
        # Automatically works for all child entities.
        attrs = ", ".join(
            f"{key}={value}"
            for key, value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({attrs})"
