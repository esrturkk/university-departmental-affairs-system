from django import forms
from django.forms.widgets import DateInput, TimeInput
from .models import Course, Classroom, ExamSchedule
from accounts.models import CustomUser

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

class ExamScheduleForm(forms.ModelForm):
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        required=True,
        label='Derslik'
    )
    invigilator = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role__title__in=['Bölüm Başkanı', 'Öğretim Elemanı']),
        required=True,
        label='Gözetmen'
    )

    class Meta:
        model = ExamSchedule
        fields = ['course', 'exam_day', 'start_time', 'end_time', 'classroom', 'invigilator', 'note']
        widgets = {
            'exam_day': DateInput(attrs={'type': 'date'}),
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
