from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseNotFound
from Salmonella.models import Isolate, Location, Isolation, View_apcc, Project
from Salmonella.views.FuncsAuxAndDb import getHeaders
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import constants as c
from Salmonella.views.FuncsAuxAndDb import queryDb as q


def page(request, pk):



	userProjIds = list()

	if request.user.is_authenticated:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)
		projHeader = det.convertToJson(c.ProjHeaderPv)
		userProjIds = q.getUserProjectIds(request.user.username)

	else:
		isoInfo = det.convertToJson(c.IsolateHeaderPu)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPu)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPu)
		projHeader = []

	# check pk refers to public strain, then return.

	isolate = None
	isoMgt = None
	json_isoMgt = {}
	isUserIso = False

	try:
		isolate = Isolate.objects.get(pk=pk)
	except Isolate.DoesNotExist:
		raise Http404("Isolate does not exist")

	if isolate.server_status == 'C' and isolate.assignment_status == 'A':
		print(str(isolate) + " !!")
		isoMgt = View_apcc.objects.get(mgt_id=isolate.mgt)

	if isoMgt:
		json_isoMgt = serializers.serialize('json', [isoMgt])




	if len(userProjIds) > 0:
		if isolate.project_id in userProjIds:
			isUserIso = True
			project = Project.objects.get(pk=isolate.project_id)




	return render(request, 'Salmonella/isolateDetail.html', {"isoHeader": isoInfo, "apHeader": apHeader, "ccHeader": ccHeader, "epiHeader": epiInfo, "locHeader": locInfo, "islnHeader": islnInfo, "isolate": isolate, "json_isoHgt": json_isoMgt, "projHeader": projHeader, "isUserIso": isUserIso}) # {"isolate": isolate, "json_isoHgt": json_isoMgt }) # }) #  "similar_strains": qs_similarAps},)
