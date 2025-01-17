# services/discounts.py
from abc import ABC


class BaseDiscount(ABC):
    """
    Represents a abstract class for purchase discounts.
    """

    def apply_discount(self, total_price):
        raise NotImplementedError("Subclasses must implement this method")


class PercentageDiscount(BaseDiscount):
    """
    Represents a percentage discounts.
    """

    def __init__(self, discount_rate):
        self.discount_rate = discount_rate

    def apply_discount(self, total_price):
        return total_price * (1 - self.discount_rate/100)


class FixedAmountDiscount(BaseDiscount):
    """
    Represents a Fixed amount of discounts.
    """

    def __init__(self, discount_amount):
        self.discount_amount = discount_amount

    def apply_discount(self, total_price):
        return max(total_price - self.discount_amount, 0)
