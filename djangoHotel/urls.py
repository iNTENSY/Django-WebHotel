"""djangoHotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from djangoHotel import settings
from main.urls import views


router = routers.SimpleRouter()
router.register('apartments-admin', views.ApartmentsAdminViewSet)
router.register('apartments', views.ApartmentsReadOnlyViewSet)
# router.register('booking', views.BookingViewSet)
# router.register('booking', views.BookingRetrieveDestroyAPIView.as_view())


urlpatterns = [
    path('admin/', admin.site.urls, name='admin-site'),
    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),

    path('api/v1/', include(router.urls)),
    path('api/v1/booking/', views.BookingListAPIView.as_view()),
    path('api/v1/booking/<int:pk>', views.BookingRetrieveDestroyAPIView.as_view()),
    path('api/v1/create_booking/', views.BookingCreateAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
