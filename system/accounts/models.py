from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, verbose_name='Rol')
    
class Staff(CustomUser):
    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.username}'

class Student(CustomUser):
    student_no = models.IntegerField(unique=True, verbose_name='Öğrenci No')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.student_no}'

class Role(models.Model):
    title = models.CharField(max_length=50, verbose_name='İsim')
    type = models.CharField(max_length=50, verbose_name='Tür')

    def __str__(self):
        return f'{self.title}-{self.type}'
    
    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roller'
