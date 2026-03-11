from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.v1.accounts.permissions import IsManager
from events.models import Event, Venue
from api.v1.events.serializers import EventSerializer, VenueSerializer
from api.v1.events.permissions import IsEventOwner
from rest_framework.response import Response
from api.v1.events.services import cancel_event_and_refund



class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticated, IsManager]

class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManager, IsEventOwner]

    def get_queryset(self):
        return Event.objects.all()
    
class PublicEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = []

    def get_queryset(self):
        return Event.objects.filter(status='published')

class CancelEventView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)

        if event.status == 'cancelled':
            return Response(
                {"message": "Event already cancelled"},
                status=400
            )

        cancel_event_and_refund(event)

        return Response({
            "message": "Event cancelled successfully. All bookings invalidated."
        })
