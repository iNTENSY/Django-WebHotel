from datetime import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from .filters import ApartmentFilter
from .models import Booking, Apartment
from common_utils.utils import TitleMixin, CheckForBookingMixin
from .permissions import IsOwnerOrAdmin
from .serializers import ApartmentSerializer, BookingSerializer


class MainPageView(TitleMixin, ListView):
    """ Отображение основной страницы """

    queryset = Apartment.objects.values('pk', 'number', 'price', 'reservation')
    template_name = 'base.html'
    context_object_name = 'rooms'


class MyFilterView(TitleMixin, ListView):
    """ Отображение страницы с фильтром """

    model: object = Apartment
    template_name: str = 'apartment_templates/filter_apartments.html'
    context_object_name: str = 'rooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context: dict = super(MyFilterView, self).get_context_data(**kwargs)
        context['filter'] = ApartmentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ReservationView(LoginRequiredMixin, CheckForBookingMixin, CreateView):
    """ Отображение страницы для бронирования"""

    model: object = Booking
    login_url: str = 'users:login'
    template_name: str = 'apartment_templates/reservation.html'
    fields: list[str] = ['room', 'start_of_booking', 'end_of_booking']

    def post(self, request, **kwargs):
        user: object = request.user
        room: Apartment = Apartment.objects.get(number=request.POST.get('room'))
        start_of_booking: dt = dt.strptime(request.POST.get('start_of_booking'), '%d.%m.%Y')
        end_of_booking: dt = dt.strptime(request.POST.get('end_of_booking'), '%d.%m.%Y')
        template_name: str = 'apartment_templates/oops.html'

        is_allowed: bool = self.check_booking(user, room, start_of_booking, end_of_booking)

        if is_allowed:
            return redirect('main:first-page')
        return render(request, template_name, {'answer': 'Комната уже забронирована!'})


class DeleteReservationView(LoginRequiredMixin, View):
    """ Удаление бронирования """

    login_url: str = 'users:login'

    def post(self, request, **kwargs):
        room_number: int = request.POST.get('room_number')
        start: dt = dt.strptime(request.POST.get('start'), '%d.%m.%Y')
        end: dt = dt.strptime(request.POST.get('end'), '%d.%m.%Y')

        booking: Booking = Booking.objects.get(room__number=room_number, start_of_booking=start, end_of_booking=end)
        booking.delete()
        return redirect(reverse('users:profile', kwargs={'pk': request.user.pk}))


class ApartmentsAdminViewSet(viewsets.ModelViewSet):
    """ ViewSet для администратора """

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = (IsAdminUser,)


class ApartmentsListAPIView(generics.ListAPIView):
    """ ViewSet для пользователя сайта """

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ApartmentFilter


class BookingCreateAPIView(CheckForBookingMixin, generics.CreateAPIView):
    """ API View для создания бронирования """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        user: str = serializer.data['customers']
        room: Apartment = Apartment.objects.get(number=serializer.data['room'])
        start_of_booking: dt = dt.strptime(serializer.data['start_of_booking'], '%Y-%m-%d')
        end_of_booking: dt = dt.strptime(serializer.data['end_of_booking'], '%Y-%m-%d')

        is_allowed: bool = self.check_booking(user, room, start_of_booking, end_of_booking)

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
    """ API View для списка всех бронирований """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAdminUser,)



class BookingRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ API View для получения бронирования для конкретного пользователя """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsOwnerOrAdmin,)
