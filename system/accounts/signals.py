from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CustomUser, Student, Role
import random

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    roles = [
        ('Bölüm Başkanı', 'İdari'),
        ('Bölüm Sekreteri', 'İdari'),
        ('Öğretim Elemanı', 'Akademik'),
    ]

    for title, role_type in roles:
        Role.objects.get_or_create(title=title, type=role_type)

@receiver(post_migrate)
def create_default_staff(sender, **kwargs):
    staff = [
        ('Ahmet', 'Yılmaz', 'ahmet.yilmaz@example.com', 1),
        ('Ayşe', 'Kara', 'ayse.kara@example.com', 2),
        ('Mehmet', 'Çelik', 'mehmet.celik@example.com', 3),
        ('Fatma', 'Demir', 'fatma.demir@example.com', 3),
        ('Emre', 'Kılıç', 'emre.kilic@example.com', 3),
    ]

    for first_name, last_name, email, role_id in staff:
        username = email.split('@')[0]
        role = Role.objects.filter(id=role_id).first()
        if not role:
            continue

        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            }
        )
        if created:
            user.set_password('1234')
            user.save()

@receiver(post_migrate)
def create_default_students(sender, **kwargs):
    first_names = [
        'Ahmet', 'Ayşe', 'Mehmet', 'Fatma', 'Emre', 'Zeynep', 'Ali', 'Merve', 'Hüseyin', 'Sedef',
        'Burak', 'Elif', 'Deniz', 'Serkan', 'Derya', 'Cem', 'Büşra', 'Gökhan', 'Ece', 'Onur',
        'Selin', 'Murat', 'Gamze', 'Tolga', 'Nazlı', 'Okan', 'Yasemin', 'Barış', 'Şule', 'Hakan'
    ]

    last_names = [
        'Yılmaz', 'Kara', 'Çelik', 'Demir', 'Kılıç', 'Aydın', 'Öztürk', 'Yıldız', 'Aslan', 'Sarı',
        'Şahin', 'Polat', 'Kurt', 'Güneş', 'Özkan', 'Yalçın', 'Turan', 'Karaoğlu', 'Çetin', 'Erdoğan',
        'Arslan', 'Eren', 'Koç', 'Doğan', 'Taş', 'Şimşek', 'Kaya', 'Can', 'Uysal', 'Baran'
    ]

    for i in range(30):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        student_no = 1000 + i + 1
        email = f'{student_no}@example.com'

        Student.objects.get_or_create(
            student_no=student_no,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
        )
