from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):
    help = 'Updates the Site domain to match the one in settings'

    def handle(self, *args, **options):
        try:
            site = Site.objects.get(id=settings.SITE_ID)
            site.domain = settings.SITE_DOMAIN
            site.name = settings.SITE_NAME
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated site domain to {settings.SITE_DOMAIN}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating site: {str(e)}'))
