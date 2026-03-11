from django.urls import path
from api.v1.seats.views import AvailableSeatsView

urlpatterns = [
    path('available/<int:event_id>/', AvailableSeatsView.as_view()),
]
