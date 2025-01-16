from http.client import responses

from django.db import transaction
from django.shortcuts import render

# views.py in `pricing` app
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItemThrough
from .services import OrderService

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import (
    RetrieveProductSerializer,
    AddProductSerializer,
    AddOrderSerializer,
    RetrieveOrderSerializer,
)


class ProductAPI(APIView):
    """
    API to create a new product and list all products.
    """

    def get(self, request):
        """Retrieve a list of all products."""
        products = Product.objects.all()
        serializer = RetrieveProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        """Create a new product."""
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            response = RetrieveProductSerializer(obj).data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderAPI(APIView):
    """
    API for creating orders and retrieving totals.
    """
    @transaction.atomic
    def post(self, request):
        serializer = AddOrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            products_with_quantities = data.get("products")
            order = Order.objects.create()

            for item in products_with_quantities:
                product = Product.objects.get(id=item["product_id"])
                OrderItemThrough.objects.create(
                    order=order, product=product, quantity=item["quantity"]
                )

            return Response(
                {
                    "order_id": order.id,
                    "total_price": OrderService(order).calculate_total(),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = RetrieveOrderSerializer(order)
            total = OrderService(order).calculate_total()
            return Response(
                {"order_id": order_id, "total_price": total, "order": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
