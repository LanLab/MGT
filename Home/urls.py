from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', views.index.page, name='index'),
	url(r'^home/$', login_required(views.home.page), name='home'),
	url(r'^about$', views.about.page, name='about'),
	url(r'^contact$', views.contact.page, name='contact'),
	url(r'^faq$', views.faq.page, name='faq'),
#	url(r'^accounts/password/reset/$', auth_views.password_reset, {'template_name': 'Home/registration/password_reset_form.html', 'email_template_name': 'Home/registration/password_reset_email.html'}, name='auth_password_reset'),
#	url(r'^accounts/password/reset/auth_password_reset_done/$', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='auth_password_reset_done'),
#	url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',auth_views.password_reset_confirm, {'template_name': 'Home/password_reset_confirm.html'}, name='auth_password_reset_confirm'),
#	url(r'^password/reset/confirm/complete/$', auth_views.password_reset_complete, {'template_name': 'Home/password_reset_complete.html'}),
]

	# url(r'^accounts/password/reset/done$', password_reset, {'template_name': 'Home/password_reset_done.html'}, name='password_reset_done'),


	# url(r'^change-password-done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}, name="password-change-done")
