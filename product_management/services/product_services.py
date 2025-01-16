class BaseProduct:
    """
    Represents a base product with a name and base price.

    Attributes:
        product (obj): The object of the product model.
        base_price (float): The base price of the product.
        quantity (int) : Number of products.
    """

    def __init__(self, product):
        self.product = product

    def get_price(self, quantity=1):
        """
        Return the base price for the product.
        """
        return self.product.base_price * quantity


class SeasonalProduct(BaseProduct):
    """
    Represents a seasonal product with a seasonal discount rate.

    Attributes:
        seasonal_discount (float): The discount rate for the product during
        seasonal sales.
    """

    def __init__(self, product, seasonal_discount):
        super().__init__(product)
        self.seasonal_discount = seasonal_discount

    def get_price(self, quantity=1):
        base_price = super().get_price(quantity)
        discount = base_price * (1 - self.seasonal_discount / 100)
        return discount


class BulkProduct(BaseProduct):
    """
    Represents a product with bulk purchase discounts.

    Attributes:
        bulk_quantity (int): The minimum quantity required for a bulk discount.
        bulk_discount_rate (float): The discount rate for bulk purchases.
    """

    def __init__(self, product, bulk_discount, bulk_quantity):
        super().__init__(product)
        self.bulk_discount = bulk_discount
        self.bulk_quantity = bulk_quantity

    def get_price(self, quantity=1):
        if quantity >= self.bulk_quantity:
            discounted_price = self.base_price * (1 - self.bulk_discount_rate)
        else:
            discounted_price = self.base_price
        return discounted_price * quantity
