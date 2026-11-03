from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("booking/<str:booking_id>/", views.registration_success, name="registration_success"),
    path("event-rules/", views.rules, name="rules"),
]
