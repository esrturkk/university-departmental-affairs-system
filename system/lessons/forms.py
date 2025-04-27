from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'course_credit', 'course_level']
        labels = {
            'course_name': 'Ad',
            'course_code': 'Kod',
            'course_credit': 'Kredi',
            'course_level': 'Seviye',
        }
