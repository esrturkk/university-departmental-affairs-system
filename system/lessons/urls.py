from django.urls import path
from .views import CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView, courseScheduleGenerator, courseScheduleViewer

urlpatterns = [
    path('', CourseListView.as_view(), name='courses'),
    path('new/', CourseCreateView.as_view(), name='course_new'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('courseSchedule/generate', courseScheduleGenerator, name='courseScheduleGenerator'),
    path('courseSchedule/view', courseScheduleViewer, name='courseScheduleViewer'),
]
