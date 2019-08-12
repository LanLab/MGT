from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from Salmonella.views.FuncsAuxAndDb import getHeaders, routeToRightFnAuth
from Salmonella.models import View_apcc, Project, User
from itertools import *
from django.db import connections
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import constants as c
from Salmonella.views.FuncsAuxAndDb import constants_local as cl
from Salmonella.views.FuncsAuxAndDb import sessionFns as ses
from Salmonella.views.FuncsAuxAndDb.makeCsvString import makeCsv
from Salmonella.views.FuncsAuxAndDb import queryDb as q
from Salmonella.views.FuncsAuxAndDb import getPoolOfCcMergeIds as getCcMergeIdsList
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from types import MethodType
from django.db.models import Q
import re


@csrf_exempt
def page(request):

	if not request.user.is_authenticated:
		raise Http404("You need to log in to view this page!")

	else:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPv)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)

	sessionVar = list()

	pageNumToGet = 1
	orderBy = None
	dir = None

	isCsv = False;
	maxIsolatesPerPage = c.TOTAL_ISO_PER_PAGE


	arr_ap = []; arr_cc = []; arr_epi = []; arr_iso = []; arr_isln = []; arr_loc = [];



	if (('orderBy' in request.POST and len(request.POST['orderBy']) > 0) or ('pageNumToGet' in request.POST and len(request.POST['pageNumToGet']) > 0)) or ('isCsv' in request.POST and request.POST['isCsv'] == 'true'):
		# get variables from session
		sessionVar_json = request.session['sessionVar']
		sessionVar = json.loads(sessionVar_json)

		if sessionVar[0]['pageType'] != cl.SearchProjectDetail:
			raise Http404()


		(arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc) = ses.loadSessionSearchVars(sessionVar)
		projectId = sessionVar[0]['projectId']

		if 'orderBy' in request.POST and len(request.POST['orderBy']) > 0:
			orderBy = request.POST['orderBy']
			dir = request.POST['dir']

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


	elif 'projectId' in request.POST and len(request.POST['projectId']) > 0  and ses.isASearchPresent(request.POST):
		# a new search has been initiated
		sessionVar.append(dict())

		(arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc, projectId) = loadRequestSearchVars_proj(request.POST) # adds project id to arr_iso

		sessionVar[0]['arrAp'] = arr_ap
		sessionVar[0]['arrCc'] = arr_cc
		sessionVar[0]['arrEpi'] = arr_epi
		sessionVar[0]['arrIso'] = arr_iso
		sessionVar[0]['arrIsln'] = arr_isln
		sessionVar[0]['arrLoc'] = arr_loc
		sessionVar[0]['projectId'] = projectId

		sessionVar[0]['pageType'] = cl.SearchProjectDetail

	else:
	 	raise Http404("Desired vars not in search")

	# CHECK! if use has the right access rights

	if not Project.objects.filter(id=int(projectId),user=User.objects.get(userId=request.user)).exists():
		return Http404("Error: you dont have permission to access this page!")



	json_sessionVar = json.dumps(sessionVar, cls=DjangoJSONEncoder)
	request.session['sessionVar'] = json_sessionVar

	#########################

	isAp = True; isDst = False; isMgtColor = True;
	if 'isAp' in request.POST and request.POST['isAp'] == "false":
		isAp = False
	if 'isDst' in request.POST and request.POST['isDst'] == 'true':
		isDst = True
	if 'isMgtColor' in request.POST and request.POST['isMgtColor'] == 'false':
		isMgtColor = False


	(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn(arr_ap, arr_cc, arr_epi, arr_loc, arr_isln, arr_iso, pageNumToGet, maxIsolatesPerPage, request.user.username, True, orderBy, dir)


	mergedIds = det.convertToJson_dict(dict_mergedIds)
	if isCsv:
		outstring = makeCsv(isolates,request.user.is_authenticated)
		return HttpResponse(outstring)
	else:
		jsonIso = det.convertToJson(isolates)

		return render(request, 'Salmonella/isolateTable.html', {"isolates": jsonIso, "IsolateId": c.IsolateId, "isAp": isAp, 'isDst': isDst, 'isMgtColor': isMgtColor, "colIsoId": c.IsolateId, "isoInfo": isoInfo, "apInfo": apHeader, "ccInfo": ccHeader, "mgtInfo": mgtInfo, "epiInfo": epiInfo, "locInfo": locInfo, "islnInfo": islnInfo, "isoCount": isoCount,  "pageInfo": dict_pageInfo, "mergedIds": mergedIds})

#################
def loadRequestSearchVars_proj(requestVar):
	arr_ap = json.loads(requestVar['arrAp'])
	arr_cc = json.loads(requestVar['arrCc'])
	arr_epi = json.loads(requestVar['arrEpi'])
	arr_iso = json.loads(requestVar['arrIso'])
	arr_isln = json.loads(requestVar['arrIsln'])
	arr_loc = json.loads(requestVar['arrLoc'])

	projectId = int (json.loads(requestVar['projectId']))

	arr_iso.append({'project': projectId })

	return (arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc, projectId)
