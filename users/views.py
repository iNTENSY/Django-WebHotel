from datetime import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView

from common_utils.utils import TitleMixin, SuperuserRequiredMixin
from main.models import Booking
from .forms import LoginForm, RegistrationForm


class UserProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    """ Отображение профиля пользователя """

    title: str = 'Профиль'
    template_name: str = 'user_templates/profile.html'
    context_object_name: str = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context: dict = super(UserProfileView, self).get_context_data()
        user_pk: int = kwargs.get('pk')
        queryset: object = Booking.objects.select_related('room').filter(customers_id=user_pk)\
            .values(
            'room__number', 'room__price', 'room__reservation',
            'start_of_booking', 'end_of_booking', 'is_accepted'
        )
        context['b_objects'] = queryset
        return context


class LoginPageView(TitleMixin, LoginView):
    """ Отображение страницы с формой для авторизации """

    title: str = 'Авторизация'
    form_class: object = LoginForm
    template_name: str = 'user_templates/login.html'

    def get_success_url(self):
        return reverse_lazy('main:first-page')


class RegistrationPageView(TitleMixin, CreateView):
    """ Отображение страницы с формой для регистрации """

    title: str = 'Регистрация'
    form_class: object = RegistrationForm
    template_name: str = 'user_templates/registration.html'

    def get_success_url(self):
        return reverse_lazy('users:login')


class LogoutButton(LogoutView):
    """ Отображение кнопки с возможностью выхода из аккаунта """

    next_page: str = reverse_lazy('main:first-page')


class EditPageView(SuperuserRequiredMixin, ListView):
    """ Отображение страницы для администраторов с возможностью принять/удалить бронирование """

    queryset: object = Booking.objects.filter(is_accepted=False).select_related('room')\
        .values(
        'room__number', 'room__price', 'room__reservation',
        'customers__username', 'start_of_booking', 'end_of_booking'
    )
    template_name: str = 'user_templates/edit_page.html'
    context_object_name: str = 'booking_list'

    def post(self, request, **kwargs):
        status: int = request.POST.get('status')
        room_number: int | None = request.POST.get('accepted_room_number', None)\
                                  or request.POST.get('denied_room_number', None)
        booking_start: str | None = request.POST.get('accepted_room_st_dt', None) \
                                    or request.POST.get('accepted_room_ed_dt', None)
        booking_end: str | None = request.POST.get('accepted_room_ed_dt', None) \
                      or request.POST.get('denied_room_ed_dt', None)

        start_of_booking: dt = dt.strptime(booking_start, '%d.%m.%Y')
        end_of_booking: dt = dt.strptime(booking_end, '%d.%m.%Y')

        booking: Booking = Booking.objects.get(
            room__number=room_number,
            start_of_booking=start_of_booking,
            end_of_booking=end_of_booking
        )

        if status == 'accept':
            booking.is_accepted = True
            booking.save()
        elif status == 'deny':
            booking.delete()

        return redirect('users:booking-edit')