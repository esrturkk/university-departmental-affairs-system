from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Course, Classroom
from accounts.models import CustomUser
import random

@receiver(post_migrate)
def create_default_lessons(sender, **kwargs):
    instructor_names = [
        ('Ahmet Yılmaz', 'ahmet.yilmaz@example.com'),
        ('Ayşe Kara', 'ayse.kara@example.com'),
        ('Mehmet Çelik', 'mehmet.celik@example.com'),
        ('Ali Öztürk', 'ali.ozturk@example.com'),
        ('Zeynep Aydın', 'zeynep.aydin@example.com'),
        ('Fatma Demir', 'fatma.demir@example.com'),
        ('Emre Kılıç', 'emre.kilic@example.com'),
        ('Sedef Sarı', 'sedef.sari@example.com'),
        ('Hüseyin Aslan', 'huseyin.aslan@example.com'),
        ('Merve Yıldız', 'merve.yildiz@example.com')
    ]
    for full_name, email in instructor_names:
        CustomUser.objects.get_or_create(
            username=email.split('@')[0],
            defaults={
                'email': email,
                'first_name': full_name.split(' ')[0],
                'last_name': full_name.split(' ')[1],
                'role_id': 3
            }
        )

    instructors = list(CustomUser.objects.filter(role_id__in=[1, 3]))

    course_names = [
        ('Matematik 1', 'MATH1'), ('Fizik 1', 'PHYS1'), ('Kimya 1', 'CHEM1'), 
        ('Bilgisayar Mühendisliği Temelleri', 'CENG'), ('Veritabanı Yönetim Sistemleri', 'DBMS'),
        ('Algoritmalar ve Veri Yapıları', 'ALGO'), ('Elektrik Devreleri', 'ELEC1'), 
        ('Olasılık ve İstatistik', 'STAT1'), ('Yapay Zeka', 'AI1'), ('Python Programlama', 'PYTHON'),
        ('Dijital Tasarım', 'DIG'), ('Ağ Teknolojileri', 'NET1'), ('İşletim Sistemleri', 'OS'),
        ('Makine Öğrenmesi', 'ML'), ('Veri Madencliği', 'DM'), 
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
                'classroom_capacity': random.choice([30, 40, 50, 60])
            }
        )
