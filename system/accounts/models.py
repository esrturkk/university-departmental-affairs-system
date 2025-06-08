from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class CustomUser(AbstractUser):
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, verbose_name='Rol')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        return reverse('staff_detail', kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name = 'personel'
        verbose_name_plural = 'personeller'

class Student(models.Model):
    student_no = models.PositiveIntegerField(unique=True, verbose_name='Öğrenci No')
    first_name = models.CharField(max_length=50, verbose_name='Ad')
    last_name = models.CharField(max_length=50, verbose_name='Soyad')
    email = models.EmailField(verbose_name='E-posta')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'öğrenci'
        verbose_name_plural = 'öğrenciler'

class Role(models.Model):
    title = models.CharField(max_length=50, verbose_name='İsim')
    type = models.CharField(max_length=50, verbose_name='Tür')

    def __str__(self):
        return f'{self.title}-{self.type}'
    
    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roller'
