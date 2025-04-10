from django.urls import path
from .views import scheduleGenerator

urlpatterns = [
    path("schedule/generate/", scheduleGenerator, name="scheduleGenerator"),
]
