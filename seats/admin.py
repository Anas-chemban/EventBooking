
from django.contrib import admin
from seats.models import Seat, SeatCategory, SeatLock
@admin.register(SeatCategory)
class SeatCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'venue', 'category', 'is_active')
    list_filter = ('venue', 'category')

@admin.register(SeatLock)
class SeatLockAdmin(admin.ModelAdmin):
    list_display = ('seat', 'event', 'user', 'locked_until')
    list_filter = ('event',)
