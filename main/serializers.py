from rest_framework import serializers

from .models import Apartment, Booking


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model: object = Apartment
        fields: tuple[str] = ('number', 'price', 'reservation', 'created_at')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model: object = Booking
        fields: str = '__all__'