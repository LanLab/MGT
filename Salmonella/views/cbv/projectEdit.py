
from django.views.generic import UpdateView
from Salmonella.models import Project, User
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django import forms


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):

	model = Project
	template_name = "Salmonella/projectEdit.html"

	fields = ['identifier',]

	def form_valid(self, form):
		if self.request.POST.get('identifier'):
			if (
				not form.cleaned_data['identifier'] or Project.objects.filter(identifier=self.request.POST.get('identifier'), user=User.objects.get(userId=self.request.user)).count() > 0
			):
				form.add_error('identifier', "Project name already exists. Please, pick another name.")
				return self.form_invalid(form)

		self.object = form.save()
		return HttpResponseRedirect(self.get_success_url())


	def get_success_url(self):
		return reverse('Salmonella:project_detail', kwargs={'pk': self.object.id})


	raise_exception = True
	def has_permission(self):
		if User.objects.filter(userId=self.request.user).count() > 0:

			if Project.objects.get(id=self.kwargs['pk']).user == User.objects.get(userId = self.request.user):
				return True

		print(self.kwargs['pk'])
		return False
