from datetime import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from .models import Booking, Apartment
from common_utils.utils import TitleMixin, CheckForBookingMixin
from .permissions import IsOwnerOrAdmin
from .serializers import ApartmentSerializer, BookingSerializer


class MainPageView(TitleMixin, ListView):
    """ Отображение основной страницы """

    queryset = Apartment.objects.values('pk', 'number', 'price', 'reservation')
    template_name = 'base.html'
    context_object_name = 'rooms'


class FilterView(TitleMixin, ListView):
    """ Отображение страницы с фильтром """

    template_name = 'apartment_templates/filter_apartments.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        r = self.request.GET
        if self.request.GET.get('filter'):
            prices = r.getlist('price', None)
            trip = r.getlist('trip', None)
            spots = r.getlist('spots', None)

            queryset = Apartment.objects.filter(
                Q(reservation__in=spots) & Q(price__range=prices)
            ).values('pk', 'number', 'price', 'reservation').exclude(
                booking__start_of_booking__range=trip, booking__end_of_booking__range=trip
            )
        else:
            queryset = Apartment.objects.all().values('pk', 'number', 'price', 'reservation')

        return queryset

    def get_count_of_spots(self):
        return Apartment.objects.values_list('reservation', flat=True).order_by('reservation').distinct()


class ReservationView(LoginRequiredMixin, CheckForBookingMixin, CreateView):
    """ Отображение страницы для бронирования"""

    model = Booking
    login_url = 'users:login'
    template_name = 'apartment_templates/reservation.html'
    fields = ['room', 'start_of_booking', 'end_of_booking']

    def post(self, request, **kwargs):
        user = request.user
        room = Apartment.objects.get(number=request.POST.get('room'))
        start_of_booking = dt.strptime(request.POST.get('start_of_booking'), '%d.%m.%Y')
        end_of_booking = dt.strptime(request.POST.get('end_of_booking'), '%d.%m.%Y')
        template_name = 'apartment_templates/oops.html'

        is_allowed = self.check_booking(user, room, start_of_booking, end_of_booking)

        if is_allowed:
            return redirect('main:first-page')
        return render(request, template_name, {'answer': 'Комната уже забронирована!'})


class DeleteReservationView(LoginRequiredMixin, View):
    """ Удаление бронирования """

    login_url = 'users:login'

    def post(self, request, **kwargs):
        room_number = request.POST.get('room_number')
        start = dt.strptime(request.POST.get('start'), '%d.%m.%Y')
        end = dt.strptime(request.POST.get('end'), '%d.%m.%Y')

        booking = Booking.objects.get(room__number=room_number, start_of_booking=start, end_of_booking=end)
        booking.delete()
        return redirect(reverse('users:profile', kwargs={'pk': request.user.pk}))


class ApartmentsAdminViewSet(viewsets.ModelViewSet):
    """ ViewSet для администратора """

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = (IsAdminUser,)


class ApartmentsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet для пользователя сайта """

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class BookingCreateAPIView(CheckForBookingMixin, generics.CreateAPIView):
    """ APIView для создания бронирования (без учета) """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        user = serializer.data['customers']
        room = Apartment.objects.get(number=serializer.data['room'])
        start_of_booking = dt.strptime(serializer.data['start_of_booking'], '%Y-%m-%d')
        end_of_booking = dt.strptime(serializer.data['end_of_booking'], '%Y-%m-%d')

        is_allowed = self.check_booking(user, room, start_of_booking, end_of_booking)

        if is_allowed:
            serializer.save()
        return is_allowed

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_allowed = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if is_allowed:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'Уже имеется запись'})


class BookingListAPIView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAdminUser,)



class BookingRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsOwnerOrAdmin,)
