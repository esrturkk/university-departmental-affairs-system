from django import forms
from .models import CustomUser, Student
from lessons.models import Course

class StaffForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Şifre'
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password']
        labels = {
            'username': 'Personel Kimliği',
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-posta',
            'role': 'Görev',
        }

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['password'].initial = ''

class StudentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
            queryset=Course.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label='Aldığı Dersler'
        )

    class Meta:
        model = Student
        fields = ['student_no', 'first_name', 'last_name', 'email', 'courses']
        labels = {
            'student_no': 'Öğrenci No',
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-posta',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['courses'].initial = self.instance.courses.all()

    def save(self, commit=True):
        student = super().save(commit)
        if commit:
            student.courses.set(self.cleaned_data['courses'])
        return student
