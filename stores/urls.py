from django.urls import path
from .views import ProductsView, OrdersView, AddProduct

urlpatterns = [
    path('all-products/', ProductsView.as_view(), name='all-products'),
    path('product/<str:id>', ProductsView.as_view(), name='product'),
    path("add-product/", AddProduct.as_view(), name="add-product"),
    path('orders/', OrdersView.as_view(), name='orders'),
]