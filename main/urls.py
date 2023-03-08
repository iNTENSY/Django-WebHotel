from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='first-page'),
    path('reserve/', views.ReservationView.as_view(), name='subscribe-button'),
    path('remove/', views.DeleteReservationView.as_view(), name='unsubscribe-button'),
    path('filter/', views.FilterView.as_view(), name='filter'),
]