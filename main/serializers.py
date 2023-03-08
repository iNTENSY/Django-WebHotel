from rest_framework import serializers

from .models import Apartment, Booking


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('number', 'price', 'reservation', 'created_at')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'