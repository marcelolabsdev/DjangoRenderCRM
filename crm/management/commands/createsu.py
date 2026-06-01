import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea un superusuario automaticamente desde variables de entorno'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USER', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superusuario ya existe: {username}'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {username}'))
