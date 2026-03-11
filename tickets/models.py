from django.db import models
from bookings.models import Booking
from django.conf import settings
from seats.models import Seat

# Create your models here.
class Ticket(models.Model):
    TICKET_STATUS = (
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUS,
        default='active'
    )

    qr_code = models.ImageField(upload_to='tickets/')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.booking.event.title} - {self.seat.seat_number}"
