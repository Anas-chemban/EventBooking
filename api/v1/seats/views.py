from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.v1.seats.selectors import available_seats
from events.models import Event


class AvailableSeatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        seats = available_seats(event)

        return Response([
            {
                "id": seat.id,
                "seat_number": seat.seat_number,
                "category": seat.category.name,
                "price": str(seat.category.price),
            }
            for seat in seats
        ])
