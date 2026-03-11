from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

from seats.models import SeatLock
LOCK_MINUTES = 10
def lock_seat(seat, event, user):
    now = timezone.now()

    with transaction.atomic():
        if SeatLock.objects.filter(
            seat=seat,
            event=event,
            locked_until__gt=now
        ).exists():
            raise ValidationError("Seat already locked")

        return SeatLock.objects.create(
            seat=seat,
            event=event,
            user=user,
            locked_until=now + timedelta(minutes=LOCK_MINUTES)
        )
