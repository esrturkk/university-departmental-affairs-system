from django import forms
from .models import Course, Classroom

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'course_credit', 'course_level', 'course_instructor']
        labels = {
            'course_name': 'Ad',
            'course_code': 'Kod',
            'course_credit': 'Kredi',
            'course_level': 'Seviye',
            'course_instructor': 'Öğretim Elemanı',
        }

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['classroom_name', 'classroom_code', 'classroom_capacity']
        labels = {
            'classroom_name': 'Ad',
            'classroom_code': 'Kod',
            'classroom_capacity': 'Kapasite',
        }
