from django.urls import path
from .views import CustomLoginView, StaffListView, StaffDetailView, StaffCreateView, StaffUpdateView, StaffDeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('staff/', StaffListView.as_view(), name='staff'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/new/', StaffCreateView.as_view(), name='staff_new'),
    path('staff/<int:pk>/edit/', StaffUpdateView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff_delete'),
]
