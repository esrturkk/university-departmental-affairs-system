from django import forms
from .models import CustomUser, Student

class StaffForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role']
        labels = {
            'username': 'Personel ID',
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-posta',
            'role': 'Görev'
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_no', 'first_name', 'last_name', 'email']
        labels = {
            'student_no': 'Öğrenci No',
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-posta',
        }
