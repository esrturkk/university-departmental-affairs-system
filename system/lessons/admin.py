from django.contrib import admin
from .models import Course, Classroom

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
