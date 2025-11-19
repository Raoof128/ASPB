import logging
import sys
from datetime import datetime, timezone
from typing import Optional


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configures the logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger("SPSecretBot")


def calculate_days_remaining(expiry_date: datetime) -> int:
    """Calculates the number of days remaining until the expiry date."""
    now = datetime.now(timezone.utc)
    # Ensure expiry_date is timezone-aware
    if expiry_date.tzinfo is None:
        expiry_date = expiry_date.replace(tzinfo=timezone.utc)

    delta = expiry_date - now
    return delta.days


def parse_iso_date(date_str: str) -> Optional[datetime]:
    """Parses an ISO 8601 date string into a datetime object."""
    if not date_str:
        return None
    try:
        # Handle Z for UTC
        date_str = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None
