from django.contrib import admin
from tickets.models import Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'seat', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('booking__user__email', 'seat__seat_number')
