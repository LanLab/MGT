
from django.views.generic.edit import DeleteView
from Salmonella.models import Project, Isolate, User
from django.urls import reverse
#from django_tables2 import SingleTableMixin

from django.contrib.auth.mixins import PermissionRequiredMixin

class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
	model = Project
	template_name = "Salmonella/projectDeleteConfirm.html"
	# success_url = "ProjectManagement/project_list"

	# table_class = IsolateTable
	# context_table_name = 'table'

	#def get_table_data(self):
	#	return [self.object]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		isolates = Isolate.objects.filter(project=self.object)

		context['isolates'] = isolates

		return context


	def get_success_url(self):
		return reverse('Salmonella:project_list')

	raise_exception = True
	def has_permission(self):
		if User.objects.filter(userId=self.request.user).count() > 0:

			if Project.objects.get(id=self.kwargs['pk']).user == User.objects.get(userId = self.request.user):
				return True

		print(self.kwargs['pk'])
		return False
