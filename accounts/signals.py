
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import UserProfile
from students.models import Student
from .utils import generate_unique_roll_no


@receiver(post_save, sender=User)
def create_user_profile_and_student(sender, instance, created, **kwargs):
    if not created:
        return

    
    role = 'ADMIN' if instance.is_staff else 'STUDENT'
    UserProfile.objects.create(user=instance, role=role)

    
    if role == 'STUDENT':
        Student.objects.get_or_create(
            user=instance,
            defaults={
                'roll_no': generate_unique_roll_no(),
                'name': instance.first_name or '',
                'email': instance.email,
            }
        )
