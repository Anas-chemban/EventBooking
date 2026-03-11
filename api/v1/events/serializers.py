from rest_framework import serializers
from events.models import Event, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'
        
class EventSerializer(serializers.ModelSerializer):
    available_slots = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'location',
            'status',
            'booking_limit',
            'venue',
            'created_by',
            'available_slots',
        )
