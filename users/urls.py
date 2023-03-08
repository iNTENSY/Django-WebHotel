from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('registration/', views.RegistrationPageView.as_view(), name='registration'),
    path('logout/', views.LogoutButton.as_view(), name='logout'),
    path('edit_booking/', views.EditPageView.as_view(), name='booking-edit')
]