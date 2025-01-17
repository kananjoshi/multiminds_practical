from product_management.services.product_services import (
    SeasonalProduct,
    BulkProduct,
    BaseProduct
)
from product_management.services.discount_services import (
    FixedAmountDiscount,
    PercentageDiscount,
    BaseDiscount
)


class OrderService:
    """
    Service class to calculate total order price with dynamic pricing and discounts.
    """

    def __init__(self, order):
        self.order = order

    def calculate_total(self):
        total = 0
        for item in self.order.orderitemthrough_set.all():
            # Determine the pricing logic
            if hasattr(item.product, "seasonal_discount"):
                pricing = SeasonalProduct(item.product, item.product.seasonal_discount)
            elif hasattr(item.product, "bulk_quantity"):
                pricing = BulkProduct(
                    item.product, item.product.bulk_discount, item.product.bulk_quantity
                )
            else:
                pricing = BaseProduct(item.product)

            price = pricing.get_price(item.quantity)

            # Apply discount if available
            if item.discount_type and item.discount_value is not None:
                if item.discount_type == "percentage":
                    discount_logic = PercentageDiscount(item.discount_value)
                elif item.discount_type == "fixed":
                    discount_logic = FixedAmountDiscount(item.discount_value)
                else:
                    discount_logic = BaseDiscount()

                price = discount_logic.apply_discount(price)

            total += price
        return total
