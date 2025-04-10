from django.contrib import admin
from .models import Course, Classroom, CourseSchedule

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'course_credit', 'course_level')
    search_fields = ('course_name', 'course_code')
    list_filter = ('course_level',)
    ordering = ('course_code',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_name', 'classroom_capacity')
    search_fields = ('classroom_name',)
    ordering = ('classroom_name',)

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'classroom', 'instructor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('course__course_name', 'instructor__username')
    ordering = ('day_of_week', 'start_time')
