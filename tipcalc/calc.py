"""Core bill-splitting logic."""


def split_bill(total: float, people: int, tip_pct: float = 10.0) -> float:
    """Return the per-person amount (total plus tip), rounded to 2 decimal places."""
    return round(total * (1 + tip_pct / 100) / people, 2)
