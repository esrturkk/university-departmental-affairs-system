from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='Ders Adı')
    course_code = models.CharField(max_length=20, unique=True, verbose_name='Ders Kodu')
    course_credit = models.PositiveIntegerField(verbose_name='Ders Kredisi')
    course_level = models.PositiveIntegerField(verbose_name='Ders Seviyesi')
    course_instructor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={
            'role__title__in': ['Öğretim Elemanı', 'Bölüm Başkanı']
        },
        verbose_name='Öğretim Elemanı veya Bölüm Başkanı'
    )

    def __str__(self):
        return f'{self.course_name} | {self.course_code}'
    
    class Meta:
        verbose_name = 'ders'
        verbose_name_plural = 'dersler'
    
class Classroom(models.Model):
    classroom_name = models.CharField(max_length=50, verbose_name='Derslik Adı')
    classroom_code = models.CharField(max_length=50, unique=True, verbose_name='Derslik Kodu')
    classroom_capacity = models.PositiveIntegerField(verbose_name='Derslik Kapasitesi')

    def __str__(self):
        return f'{self.classroom_name} | {self.classroom_code}'
    
    class Meta:
        verbose_name = 'derslik'
        verbose_name_plural = 'derslikler'

class CourseSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('Pzt', 'Pazartesi'),
        ('Sal', 'Salı'),
        ('Çrş', 'Çarşamba'),
        ('Prş', 'Perşembe'),
        ('Cum', 'Cuma'),
        ('Cmt', 'Cumartesi'),
        ('Pzr', 'Pazar'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Ders')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Derslik')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, verbose_name='Günler')
    start_time = models.TimeField(verbose_name='Başlama Saati')
    end_time = models.TimeField(verbose_name='Bitiş Saati')

    def __str__(self):
        return f'{self.course.course_name} | {self.get_day_of_week_display()} | {self.start_time}'
    
    class Meta:
        verbose_name = 'ders programı'
        verbose_name_plural = 'ders programları'

class ExamSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Ders')
    exam_day = models.DateField(verbose_name='Sınav Günü')
    start_time = models.TimeField(verbose_name='Başlama Saati')
    end_time = models.TimeField(verbose_name='Bitiş Saati')
    note = models.TextField(blank=True, null=True, verbose_name='Açıklama')

    def __str__(self):
        return f'{self.course.course_name} | {self.exam_day}'
    
    class Meta:
        verbose_name = 'sınav programı'
        verbose_name_plural = 'sınav programları'

class InvigilatorAssignment(models.Model):
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, verbose_name='Sınav')
    invigilator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Görevli')

    def __str__(self):
        return f'Görevli: {self.invigilator.username} | Ders: {self.exam.course.course_name}'
    
    class Meta:
        verbose_name = 'görevli ataması'
        verbose_name_plural = 'görevli atamaları'

class ExamSeatingArrangement(models.Model):
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, verbose_name='Sınav')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Derslik')
    student_number = models.CharField(max_length=20, verbose_name='Öğrenci No')
    seat_number = models.PositiveIntegerField(verbose_name='Sıra No')

    def __str__(self):
        return f'{self.student_number} | {self.classroom.classroom_name} | {self.seat_number}'
    
    class Meta:
        verbose_name = 'sınav oturma düzeni'
        verbose_name_plural = 'sınav oturma düzenleri'
