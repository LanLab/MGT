from django.conf import settings

def root_url(request):
    """
    Pass your root_url from the settings.py
    """
    return {'SITE_URL': settings.MY_URL}
