from django.urls import path
from .views import SignUpView, CustomLoginView
from lessons.views import generate_schedule

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),

]
