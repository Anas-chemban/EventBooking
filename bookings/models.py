from django.db import models
from django.conf import settings
from django.utils import timezone
from events.models import Event


class Booking(models.Model):
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("not_started", "Not Started"),
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
        default="not_started"
    )

    payment_reference = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField(
        help_text="Seat lock expiry time"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                condition=models.Q(status='confirmed'),
                name='unique_confirmed_booking_per_user_event'
            )
        ]

    def is_expired(self):
        return timezone.now() > self.expires_at

    def can_confirm(self):
        return (
            self.status == 'pending'
            and not self.is_expired()
            and self.event.can_book()
        )

    def mark_expired(self):
        if self.status == 'pending':
            self.status = 'expired'
            self.save(update_fields=['status'])

    def __str__(self):
        return f"{self.user.email} → {self.event.title} ({self.status})"
