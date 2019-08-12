from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Salmonella.views.FuncsAuxAndDb import getHeaders, routeToRightFnAuth
from Salmonella.models import View_apcc
from itertools import *
from django.db import connections
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from functools import reduce
import operator
from Salmonella.views.FuncsAuxAndDb import getHeaders
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import constants as c
from Salmonella.views.FuncsAuxAndDb import constants_local as cl
from Salmonella.views.FuncsAuxAndDb import queryDb as q
from Salmonella.views.FuncsAuxAndDb.makeCsvString import makeCsv
from Salmonella.views.FuncsAuxAndDb import ownPaginator as ownPaginator
from Salmonella.views.FuncsAuxAndDb import sessionFns as ses
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from types import MethodType
from django.contrib.auth.decorators import login_required
from Salmonella.models import Project, User
from django.http import Http404
import re

@csrf_exempt
@login_required
def page(request):
	# print("over here .... :)")
	# print(request.POST['isAp'])

	if not request.user.is_authenticated:
		raise Http404("You need to log in to view this page!")


	if request.user.is_authenticated:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPv)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)

	sessionVar = list()

	# resent searchVar (only check if pageNumToGet or OrderBy is provided)
	pageNumToGet = 1
	orderBy = None
	dir = None
	projectId = None;

	isCsv = False;
	maxIsolatesPerPage = c.TOTAL_ISO_PER_PAGE




		# print("Come on over here.." + projectId)

	if (('orderBy' in request.POST and len(request.POST['orderBy']) > 0) or ('pageNumToGet' in request.POST and len(request.POST['pageNumToGet']) > 0)) or ('isCsv' in request.POST and request.POST['isCsv'] == 'true'):

		# session var should be reused and updated
		sessionVar_json = request.session['sessionVar']
		sessionVar = json.loads(sessionVar_json)

		if sessionVar[0]['pageType'] != cl.InitialProjIsolates:
			raise Http404()

		projectId = sessionVar[0]['projectId']

		if 'orderBy' in request.POST and len(request.POST['orderBy']) > 0:
			orderBy = request.POST['orderBy']
			dir = request.POST['dir']

			print(orderBy + " . ... . " + dir)
			# update session with posted values
			sessionVar[0]['orderBy'] = orderBy
			sessionVar[0]['dir'] = dir

			pageNumToGet = ses.loadIfInSession(sessionVar, 'pageNumToGet', 1)

		if 'pageNumToGet' in request.POST and len(request.POST['pageNumToGet']) > 0:
			pageNumToGet = int(request.POST['pageNumToGet'])

			# update session with posted values
			sessionVar[0]['pageNumToGet'] = pageNumToGet

			orderBy = ses.loadIfInSession(sessionVar, 'orderBy', None)
			dir = ses.loadIfInSession(sessionVar, 'dir', None)

		if ('isCsv' in request.POST and request.POST['isCsv'] == 'true'):
			isCsv = True;
			maxIsolatesPerPage = c.TOTAL_ISO_PER_DOWNLOAD


	elif 'projectId' in request.POST:
		# session var is new.
		sessionVar.append(dict())

		projectId = json.loads(request.POST['projectId'])


		# update session
		sessionVar[0]['projectId'] = projectId
		sessionVar[0]['pageType'] = cl.InitialProjIsolates


	else:
		raise Http404()

	# CHECK! if use has the right access rights
	if not Project.objects.filter(id=int(projectId),user=User.objects.get(userId=request.user)).exists():
		return Http404("Error: you dont have permission to access this page!")


	json_sessionVar = json.dumps(sessionVar, cls=DjangoJSONEncoder)
	request.session['sessionVar'] = json_sessionVar


	isAp = True; isDst = False; isMgtColor = True;
	if 'isAp' in request.POST and request.POST['isAp'] == "false":
		isAp = False
	if 'isDst' in request.POST and request.POST['isDst'] == 'true':
		isDst = True
	if 'isMgtColor' in request.POST and request.POST['isMgtColor'] == 'false':
		isMgtColor = False

	# get the isolates
	(isoCount, isolates, dict_pageInfo, dict_mergedIds)= routeToRightFnAuth.getIsolatesFromRightFn([], [], [], [], [], [{'project': projectId}], pageNumToGet, maxIsolatesPerPage, request.user.username, True, orderBy, dir)



	if isCsv:
		outstring = makeCsv(isolates,request.user.is_authenticated)
		return HttpResponse(outstring)
	else:

		isolatesjson = det.convertToJson(isolates)

		return render(request, 'Salmonella/isolateTable.html', {"isolates": isolatesjson, "isoCount": isoCount, "pageInfo": dict_pageInfo, "isAp": isAp, 'isDst': isDst, 'isMgtColor': isMgtColor, "colIsoId": c.IsolateId, "isoInfo": isoInfo, "apInfo": apHeader, "ccInfo": ccHeader, "mgtInfo": mgtInfo, "epiInfo": epiInfo, "locInfo": locInfo, "islnInfo": islnInfo})
