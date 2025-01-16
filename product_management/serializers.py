from rest_framework import serializers
from product_management.models import Product, Order, OrderItemThrough


class AddProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, error_messages={"required": "Product name is required."}
    )

    base_price = serializers.DecimalField(
        required=True,
        decimal_places=2,
        max_digits=10,
        error_messages={"required": "Product name is required."},
    )

    class Meta:
        model = Product
        fields = ("name", "base_price")


class RetrieveProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        model = Product
        fields = ("id", "name", "base_price")


class AddOrderItemSerializer(serializers.Serializer):
    """
    Serializer for adding products to an order.
    """

    product_id = serializers.IntegerField(
        required=True,
        error_messages={"required": "Product ID is required."},
    )
    quantity = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "Quantity is required.",
            "min_value": "Quantity must be at least 1.",
        },
    )


class AddOrderSerializer(serializers.Serializer):
    """
    Serializer for adding a new order.
    """

    products = AddOrderItemSerializer(
        many=True,
        required=True,
        error_messages={"required": "Products list is required."},
    )


class RetrieveOrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving order items with product details.
    """

    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemThrough
        fields = ["product", "quantity"]

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "base_price": obj.product.base_price,
        }


class RetrieveOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving order details.
    """

    items = RetrieveOrderItemSerializer(source="orderitemthrough_set", many=True)

    class Meta:
        model = Order
        fields = ["id", "items"]
