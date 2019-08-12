
from django.views.generic.edit import DeleteView
from Salmonella.models import Isolate, User
from django.urls import reverse
#from django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class IsolateDeleteView(PermissionRequiredMixin, DeleteView):
	model = Isolate
	template_name = "Salmonella/isolateDeleteConfirm.html"
	# success_url = "ProjectManagement/project_list"

	# table_class = IsolateTable
	# context_table_name = 'table'

	#def get_table_data(self):
	#	return [self.object]


	def get_success_url(self):
		return reverse('Salmonella:project_detail', kwargs={'pk': self.object.project.id})




	raise_exception = True
	def has_permission(self):
		if User.objects.filter(userId=self.request.user).count() > 0:

			if Isolate.objects.get(id=self.kwargs['pk']).project.user == User.objects.get(userId=self.request.user):
				return True

		print(self.kwargs['pk'])
		return False
