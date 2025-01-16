from django.urls import path

from product_management.views import OrderAPI, ProductAPI

urlpatterns = [
    path('', ProductAPI.as_view(), name='product'),
    path('order/', OrderAPI.as_view(), name='create-order'),
    path('order/<int:order_id>/', OrderAPI.as_view(), name='get-order-total'),
]