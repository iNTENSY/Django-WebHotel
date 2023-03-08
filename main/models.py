from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Apartment(models.Model):
    """ Модель для апартаментов """

    number = models.CharField('Название/номер комнаты', max_length=50, unique=True)
    price = models.DecimalField('Стоимость за сутки', decimal_places=2, max_digits=8)
    reservation = models.PositiveSmallIntegerField('Кол-во мест', default=1)
    update_at = models.DateTimeField('Обновлено', auto_now=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Апартаменты'
        verbose_name_plural = 'Апартаменты'
        ordering = ['number']

    def __str__(self):
        return f'Комната #{self.number}'


class Booking(models.Model):
    """ Модель для бронирования """

    room = models.ForeignKey(Apartment, verbose_name='Комната', on_delete=models.CASCADE)
    customers = models.ForeignKey(User, verbose_name='Клиент', on_delete=models.CASCADE)
    start_of_booking = models.DateField('Дата заезда', default=now)
    end_of_booking = models.DateField('Дата освобождения', default=now() + timedelta(days=1))
    is_accepted = models.BooleanField('Статус', default=False)
    update_at = models.DateTimeField('Обновлено', auto_now=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Резервация'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Резервация комнаты #{self.room.number}'