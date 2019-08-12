from django.views.generic.list import ListView
from Salmonella.models import Project, User
from django.db.models import Count


class ProjectListView(ListView):
	model = Project
	template_name = "Salmonella/projectList.html"

	def get_queryset(self):
		if User.objects.filter(userId=self.request.user).count() > 0:
			userObj = User.objects.get(userId=self.request.user)

			return Project.objects.filter(user=userObj).annotate(isolate_count=Count('isolate'))
		else:
			return list()
