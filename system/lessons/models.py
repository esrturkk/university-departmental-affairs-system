from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    course_credit = models.IntegerField()
    course_level = models.IntegerField()

    def __str__(self):
        return f'Ders: {self.course_name} | Kod: {self.course_code}'

    
class Classroom(models.Model):
    classroom_name = models.CharField(max_length=50, unique=True)
    classroom_capacity = models.IntegerField()

    def __str__(self):
        return f'Sınıf: {self.classroom_name} | Kapasite: {self.classroom_capacity}'
    


class CourseSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'Ders: {self.course.course_name} | Gün: {self.get_day_of_week_display()} | Saat: {self.start_time}'

class ExamSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Ders: {self.course.course_name} | Gün: {self.exam_day}'

class InvigilatorAssignment(models.Model):
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    invigilator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Görevli: {self.invigilator.username} | Ders: {self.exam.course.course_name}'


class ExamSeatingArrangement(models.Model):
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=20)
    seat_number = models.IntegerField()

    def __str__(self):
        return f'Öğrenci: {self.student_number} | Sıra: {self.seat_number} | Sınıf: {self.classroom.classroom_name}'


class InstructorSchedule(models.Model):
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'Görevli: {self.instructor.username} | Ders: {self.course.course_name} | Gün: {self.get_day_of_week_display()}'
