from django.db import models

class Product(models.Model):
    """
    Product model to store basic product information.
    """
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    """
    Order model to store order information.
    """
    products = models.ManyToManyField(Product, through='OrderItemThrough')

    def __str__(self):
        return f"Order {self.id}"

class OrderItemThrough(models.Model):
    """
    Intermediate model to manage products in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount_type = models.CharField(
        max_length=20,
        choices=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount'),
        ],
        null=True,
        blank=True,
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"