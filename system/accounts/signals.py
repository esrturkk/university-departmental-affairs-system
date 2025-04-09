from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    default_roles = [
        ('Bölüm Başkanı', 'İdari'),
        ('Bölüm Sekreteri', 'İdari'),
        ('Öğretim Elemanı', 'Akademik'),
    ]

    for title, role_type in default_roles:
        Role.objects.get_or_create(title=title, type=role_type)