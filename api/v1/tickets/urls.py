from django.urls import path
from api.v1.tickets.views import TicketCheckInView, MyTicketsView

urlpatterns = [
    path('check-in/<int:ticket_id>/', TicketCheckInView.as_view()),
    path('my/', MyTicketsView.as_view()),
]
