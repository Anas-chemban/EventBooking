from django.urls import path
from api.v1.bookings.views import (
    CreateBookingView,
    CancelBookingView,
    ForceCancelBookingView,
    MyBookingsView,
)

urlpatterns = [
    path('create/', CreateBookingView.as_view()),
    path('<int:booking_id>/cancel/', CancelBookingView.as_view()),
    path('my/', MyBookingsView.as_view()),
    path("<int:booking_id>/force-cancel/", ForceCancelBookingView.as_view()),
]
