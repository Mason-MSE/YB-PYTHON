from datetime import datetime
from typing import Optional
@staticmethod
def _parse_date(date_input: Optional[datetime | str]) -> Optional[datetime]:
    """Safely convert string (ISO format) to datetime, or return None/datetime as-is"""
    if date_input is None:
        return None
    if isinstance(date_input, datetime):
        return date_input
    if isinstance(date_input, str):
        try:
            # Handles both '2026-02-01' and '2026-02-01 14:30:00'
            return datetime.fromisoformat(date_input.replace(" ", "T") if " " in date_input else date_input)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {date_input}. Use ISO format (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)") from e
    raise TypeError(f"Unsupported date type: {type(date_input)}")       