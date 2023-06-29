import django_filters
from django.db.models import Q

from .models import Apartment


class ApartmentFilter(django_filters.FilterSet):
    booking__start_of_booking: django_filters = django_filters.DateFilter(label='Дата заезда')
    booking__end_of_booking: django_filters = django_filters.DateFilter(label='Дата выезда')
    price: django_filters = django_filters.NumberFilter(lookup_expr='lte')

    def filter_queryset(self, queryset):
        if self.data.get('booking__start_of_booking') and self.data.get('booking__end_of_booking'):
            return Apartment.objects.all().exclude(
                Q(booking__start_of_booking__gte=self.data.get('booking__start_of_booking')) |
                Q(booking__end_of_booking__lte=self.data.get('booking__end_of_booking'))
            )
        return super(ApartmentFilter, self).filter_queryset(queryset)

    class Meta:
        model = Apartment
        fields = ('reservation',)