from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management import call_command

class Command(RunserverCommand):
    help = 'Runs the server after creating a superuser if none exists'

    def handle(self, *args, **options):
        # First create superuser if needed
        call_command('create_superuser_if_none')
        
        # Then run the standard runserver command
        super().handle(*args, **options)
