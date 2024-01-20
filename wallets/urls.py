from django.urls import path
from .views import WebhookView, LoadWalletAPIView

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook-view'),
    path('wallet/load', LoadWalletAPIView.as_view(), name='load-wallet'),
]
