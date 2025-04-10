from django import forms
from .models import CustomUser

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
