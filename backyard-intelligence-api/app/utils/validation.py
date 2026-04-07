"""Input validation helpers."""

import re


US_ADDRESS_PATTERN = re.compile(r"^\s*\d+\s+.+,\s*.+,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\s*$", re.IGNORECASE)


def is_valid_us_address(address: str) -> bool:
    """Very basic US address validation for API guardrails."""
    return bool(US_ADDRESS_PATTERN.match(address))
