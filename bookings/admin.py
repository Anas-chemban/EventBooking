from django.contrib import admin
from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'status', 'created_at','payment_status','payment_reference')
    list_filter = ('status',)
    search_fields = ('user__email', 'event__title')
