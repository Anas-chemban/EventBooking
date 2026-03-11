from django.urls import path
from api.v1.payments.views import CreatePaymentOrderView
from api.v1.payments.webhooks import razorpay_webhook

urlpatterns = [
    path("create-order/", CreatePaymentOrderView.as_view()),
    path("webhook/", razorpay_webhook),
]