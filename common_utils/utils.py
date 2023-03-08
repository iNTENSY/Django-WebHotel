from django.contrib.auth.mixins import UserPassesTestMixin

from main.models import Booking


class TitleMixin:
    title = 'EmphaHotel'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CheckForBookingMixin:
    def check_booking(self, user, room, start_of_booking, end_of_booking) -> bool:
        booking = Booking.objects.filter(
            room=room,
            start_of_booking__range=(start_of_booking, end_of_booking),
            end_of_booking__range=(start_of_booking, end_of_booking),
            is_accepted=True
        )

        if booking:
            return False
        else:
            record = Booking.objects.create(
                room=room,
                customers=user,
                start_of_booking=start_of_booking,
                end_of_booking=end_of_booking
            )
            return True
