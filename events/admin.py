from django.contrib import admin
from events.models import Event, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_time', 'created_by')
    list_filter = ('status',)
    search_fields = ('title',)
