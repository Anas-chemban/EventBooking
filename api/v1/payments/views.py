from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from bookings.models import Booking
from .services import create_payment_order


class CreatePaymentOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        booking_id = request.data.get("booking_id")

        if not booking_id:
            return Response(
                {"error": "booking_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = Booking.objects.get(
            id=booking_id,
            user=request.user
        )

        order = create_payment_order(booking)

        return Response({
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "razorpay_key": "rzp_test_xxxxx"
        })