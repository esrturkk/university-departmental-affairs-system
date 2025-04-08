from django.urls import path
from .views import generate_schedule

urlpatterns = [
    path("schedule/", generate_schedule, name="generate_schedule"),
]
