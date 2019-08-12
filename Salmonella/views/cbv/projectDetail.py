
from django.views.generic.detail import DetailView
from Salmonella.models import Project, Isolate, User, Tables_ap
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import constants as c
from Salmonella.views.FuncsAuxAndDb import getHeaders

class ProjectDetailView(PermissionRequiredMixin, DetailView):

	model = Project
	template_name = "Salmonella/projectDetail.html"

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)

		context['isoHeader'] = det.convertToJson(c.IsolateHeaderPv)
		context['apHeader'] = getHeaders.getApHeaderAsJson()
		context['ccHeader'] = getHeaders.getCcHeaderAsJson()
		context['epiHeader'] = getHeaders.getEpiHeaderAsJson()
		context['locHeader'] = det.convertToJson(c.IsoMetaLocInfoPv)
		context['islnHeader'] = det.convertToJson(c.IsoMetaIslnInfoPv)
		return context


	raise_exception = True
	def has_permission(self):
		if User.objects.filter(userId=self.request.user).count() > 0:

			if Project.objects.get(id=self.kwargs['pk']).user == User.objects.get(userId = self.request.user):
				return True

		print(self.kwargs['pk'])
		return False
