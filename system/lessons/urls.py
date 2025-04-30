from django.urls import path
from .views import CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView, courseScheduleGenerator, courseScheduleViewer
from .views import ClassroomListView, ClassroomDetailView, ClassroomCreateView, ClassroomUpdateView, ClassroomDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), name='courses'),
    path('new/', CourseCreateView.as_view(), name='course_new'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('courseSchedule/generate', courseScheduleGenerator, name='courseScheduleGenerator'),
    path('courseSchedule/view', courseScheduleViewer, name='courseScheduleViewer'),
    path('classrooms/', ClassroomListView.as_view(), name='classrooms'),
    path('classroom/<int:pk>/', ClassroomDetailView.as_view(), name='classroom_detail'),
    path('classroom/new/', ClassroomCreateView.as_view(), name='classroom_new'),
    path('classroom/<int:pk>/edit/', ClassroomUpdateView.as_view(), name='classroom_edit'),
    path('classroom/<int:pk>/delete/', ClassroomDeleteView.as_view(), name='classroom_delete'),
]
