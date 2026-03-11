from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'id',
            'event',
            'status',
            'created_at',
            'expires_at',
        )
        read_only_fields = ('status', 'created_at', 'expires_at')
