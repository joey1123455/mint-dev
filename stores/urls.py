from django.urls import path
from .views import ProductsView, OrdersView

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/{product_id}', ProductsView.as_view(), name='product'),
    path('orders/', OrdersView.as_view(), name='orders'),
]