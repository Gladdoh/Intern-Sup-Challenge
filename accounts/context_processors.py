from django.conf import settings

def site_domain(request):
    """
    Adds site_domain to the context to be used in emails and templates.
    """
    protocol = 'https' if request.is_secure() else 'http'
    return {
        'site_domain': settings.SITE_DOMAIN,
        'protocol': protocol,
        'site_name': settings.SITE_NAME,
    }
