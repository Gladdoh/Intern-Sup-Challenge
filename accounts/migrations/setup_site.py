from django.db import migrations
from django.conf import settings


def update_site_name(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    # Update or create the default site
    site, created = Site.objects.update_or_create(
        id=getattr(settings, 'SITE_ID', 1),
        defaults={
            'domain': getattr(settings, 'SITE_DOMAIN', 'example.com'),
            'name': getattr(settings, 'SITE_NAME', 'example.com'),
        }
    )


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('accounts', '0004_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.RunPython(update_site_name),
    ]
