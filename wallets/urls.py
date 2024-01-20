from django.urls import path
from .views import WebhookView, LoadWalletAPIView, WithdrawWalletAPIView

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook-view'),
    path('wallet/load', LoadWalletAPIView.as_view(), name='load-wallet'),
    path('wallet/remove', WithdrawWalletAPIView.as_view(), name='remove-wallet'),
]
