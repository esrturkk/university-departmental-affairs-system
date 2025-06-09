from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Course, Classroom
from accounts.models import CustomUser, Role
import random

@receiver(post_migrate)
def create_default_courses_classrooms(sender, **kwargs):
    roles = Role.objects.filter(title__in=['Bölüm Başkanı', 'Öğretim Elemanı'])
    instructors = list(CustomUser.objects.filter(role__in=roles))

    course_names = [
        ('Matematik 1', 'MATH1'), ('Fizik 1', 'PHYS1'), ('Kimya 1', 'CHEM1'), 
        ('Bilgisayar Mühendisliği Temelleri', 'CENG'), ('Veritabanı Yönetim Sistemleri', 'DBMS'),
        ('Algoritmalar ve Veri Yapıları', 'ALGO'), ('Elektrik Devreleri', 'ELEC1'), 
        ('Olasılık ve İstatistik', 'STAT1'), ('Yapay Zeka', 'AI1'), ('Python Programlama', 'PYTHON'),
        ('Dijital Tasarım', 'DIG'), ('Ağ Teknolojileri', 'NET1'), ('İşletim Sistemleri', 'OS'),
        ('Makine Öğrenmesi', 'ML'), ('Veri Madenciliği', 'DM'), 
        ('Mobil Programlama', 'MOBILE'), ('Bilgisayar Grafikleri', 'CG'),
        ('Yazılım Mühendisliği', 'SENG'), ('Proje Yönetimi', 'PM1'), 
        ('İnternet Programlama', 'WEB'), ('Veri Tabanı Tasarımı', 'DBD'),
        ('Matematik 2', 'MATH2'), ('Fizik 2', 'PHYS2'), ('Kimya 2', 'CHEM2'),
        ('Elektrik ve Manyetizma', 'ELEC2'), ('İstatistiksel Veri Analizi', 'STAT2'),
        ('İleri Matematik', 'MATH3'), ('Makine Öğrenmesi Uygulamaları', 'MLAP'),
        ('Yapay Sinir Ağları', 'ANN'), ('C Programlama', 'C')
    ]

    for course_name, course_code in course_names:
        instructor = random.choice(instructors) if instructors else None
        Course.objects.get_or_create(
            course_code=course_code,
            defaults={
                'course_name': course_name,
                'course_credit': random.choice([1, 2, 3, 4, 5, 6]),
                'course_level': random.choice([1, 2, 3, 4]),
                'course_instructor': instructor
            }
        )

    classroom_names = [
        ('Derslik A', '1'), ('Derslik B', '2'), ('Derslik C', '3'), ('Derslik D', '4'), ('Derslik E', '5'), ('Derslik F', '6'), ('Derslik G', '7')
    ]
    for classroom_name, classroom_code in classroom_names:
        Classroom.objects.get_or_create(
            classroom_code=classroom_code,
            defaults={
                'classroom_name': classroom_name,
                'classroom_capacity': random.choice([10, 20, 30, 40])
            }
        )
