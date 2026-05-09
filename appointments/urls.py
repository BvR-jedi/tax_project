from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('request/', views.request_appointment, name='request_appointment'),
    path('request/success/', views.request_success, name='request_success'),
]
