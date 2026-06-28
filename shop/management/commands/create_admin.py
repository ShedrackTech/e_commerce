# shop/management/commands/create_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
User = get_user_model()
class Command(BaseCommand):
    help = 'Idempotently create a superuser from environment variables'
    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email    = os.environ.get('ADMIN_EMAIL',    'shedrackugwu01@gmail.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" created successfully.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'Superuser "{username}" already exists – skipping.'
            ))