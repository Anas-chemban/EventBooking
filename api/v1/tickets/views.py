from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from tickets.models import Ticket
from api.v1.tickets.services import check_in_ticket


class TicketCheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        check_in_ticket(ticket)
        return Response(
            {"message": "Ticket checked in successfully"},
            status=status.HTTP_200_OK
        )
class MyTicketsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(
            booking__user=request.user
        )

        data = [
            {
                "ticket_id": t.id,
                "event": t.booking.event.title,
                "seat": t.seat.seat_number,
                "status": t.status,
            }
            for t in tickets
        ]

        return Response(data)
