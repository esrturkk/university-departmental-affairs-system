from django.contrib import admin
from .models import Course, CourseStudent, Classroom

# Register your models here.

class StudentInline(admin.TabularInline):
    model = CourseStudent
    extra = 1
    verbose_name = 'Öğrenci'
    verbose_name_plural = 'Öğrenciler'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'course_credit', 'course_level',)
    search_fields = ('course_name', 'course_code',)
    list_filter = ('course_level',)
    ordering = ('course_code',)
    inlines = [StudentInline]

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_name', 'classroom_capacity',)
    search_fields = ('classroom_name',)
    ordering = ('classroom_name',)
