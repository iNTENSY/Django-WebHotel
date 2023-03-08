from django.contrib import admin

from . import models


@admin.register(models.Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'price', 'reservation', 'update_at', 'created_at')
    readonly_fields = ('created_at', 'update_at')


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'customers', 'start_of_booking', 'end_of_booking', 'update_at', 'created_at', 'is_accepted')
    readonly_fields = ('created_at', 'update_at')