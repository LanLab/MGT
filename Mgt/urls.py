"""Mgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static


# from Home import views as home
# from ProjectManagement import views as projectManagement

urlpatterns = [
	# url(r'^admin/', admin.site.urls),
	url(r'', include(('Home.urls', 'Home'))),
	url(r'^[sS]almonella/', include(('Salmonella.urls', 'Salmonella'))),
	url(r'^[vV]ibrio/', include(('Vibrio.urls', 'Vibrio'))),
	url(r'^accounts/', include('django_registration.backends.activation.urls')),
	url(r'^accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Broken registration urls fixed at: https://github.com/tutumcloud/django-registration/blob/master/registration/auth_urls.py
