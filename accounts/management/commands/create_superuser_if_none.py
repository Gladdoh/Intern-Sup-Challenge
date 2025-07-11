from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if no superuser exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            try:
                email = 'gladystbarasa@gmail.com'
                username = 'admin'
                password = 'Gladys@2030'

                user = User.objects.create_superuser(
                    email=email,
                    username=username,
                    password=password
                )
                
                # Make sure email is verified for the superuser
                user.email_verified = True
                user.save()
                
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" with email "{email}" created successfully!'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING('Failed to create superuser. This may happen if a user with the same email or username already exists.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists. No new superuser created.'))
