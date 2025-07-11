from django.urls import path
from .views import CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView
from .views import course_schedule_generate, course_schedule_view, exam_schedule_generate_view, exam_schedule_delete, exam_seating
from .views import ClassroomListView, ClassroomDetailView, ClassroomCreateView, ClassroomUpdateView, ClassroomDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), name='courses'),
    path('new/', CourseCreateView.as_view(), name='course_new'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('schedule/generate', course_schedule_generate, name='course_schedule_generate'),
    path('schedule/view/', course_schedule_view, name='course_schedule_view'),
    path('schedule/view/<int:user_id>', course_schedule_view, name='course_schedule_view'),
    path('exams/schedule/', exam_schedule_generate_view, name='exam_schedule'),
    path('exams/schedule/delete/<int:exam_id>/', exam_schedule_delete, name='exam_schedule_delete'),
    path('exams/schedule/<int:exam_id>/', exam_seating, name='exam_seating'),
    path('classrooms/', ClassroomListView.as_view(), name='classrooms'),
    path('classroom/<int:pk>/', ClassroomDetailView.as_view(), name='classroom_detail'),
    path('classroom/new/', ClassroomCreateView.as_view(), name='classroom_new'),
    path('classroom/<int:pk>/edit/', ClassroomUpdateView.as_view(), name='classroom_edit'),
    path('classroom/<int:pk>/delete/', ClassroomDeleteView.as_view(), name='classroom_delete'),
]
