from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = "Create a superuser from environment variables"

    def handle(self, *args, **kwargs):
        username = os.environ.get("DJANGO_SU_NAME")
        password = os.environ.get("DJANGO_SU_PASSWORD")
        email = os.environ.get("DJANGO_SU_EMAIL", "")

        if not username or not password:
            self.stdout.write("Superuser environment variables not set")
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write("Superuser created successfully")
        else:
            self.stdout.write("Superuser already exists")
