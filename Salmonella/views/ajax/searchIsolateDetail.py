from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from Salmonella.views.FuncsAuxAndDb import getHeaders, routeToRightFnAuth
from Salmonella.models import View_apcc, Project
from itertools import *
from django.db import connections
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import queryDb
from Salmonella.views.FuncsAuxAndDb.makeCsvString import makeCsv
from Salmonella.views.FuncsAuxAndDb import constants as c
from Salmonella.views.FuncsAuxAndDb import constants_local as cl
from Salmonella.views.FuncsAuxAndDb import queryDb as q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from types import MethodType
# from Salmonella.views.FuncsAuxAndDb import routeToRightFn as routeToFn
# from Salmonella.views.FuncsAuxAndDb import routeToRightFnAuth as routeToFnAuth
from Salmonella.views.FuncsAuxAndDb import getPoolOfCcMergeIds as getCcMergeIdsList
from django.db.models import Q
from Salmonella.views.FuncsAuxAndDb import sessionFns as ses


@csrf_exempt
def page(request):
	# print("yes in this page...")
	if request.user.is_authenticated:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPv)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)

	else:
		isoInfo = det.convertToJson(c.IsolateHeaderPu)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPu)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPu)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPu)



	isAp = True; isDst = False; isMgtColor = True;
	if 'isAp' in request.POST and request.POST['isAp'] == "false":
		isAp = False
	if 'isDst' in request.POST and request.POST['isDst'] == 'true':
		isDst = True
	if 'isMgtColor' in request.POST and request.POST['isMgtColor'] == 'false':
		isMgtColor = False



	sessionVar = list()

	pageNumToGet = 1
	orderBy = None
	dir = None

	isCsv = False;
	maxIsolatesPerPage = c.TOTAL_ISO_PER_PAGE


	searchAp = []; searchCcEpi = []; searchLocs = []; searchIsln = []; searchProj = [];


	if (('orderBy' in request.POST and len(request.POST['orderBy']) > 0) or ('pageNumToGet' in request.POST and len(request.POST['pageNumToGet']) > 0))or ('isCsv' in request.POST and request.POST['isCsv'] == 'true'):

		sessionVar_json = request.session['sessionVar']
		sessionVar = json.loads(sessionVar_json)

		if sessionVar[0]['pageType'] != cl.SearchIsolateDetail:
			raise Http404()

		(searchAp, searchCcEpi, searchLocs, searchIsln, searchProj) = ses.loadSessionSearchVars_detail(sessionVar)



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



	elif ses.isASearchPresent_detail(request.POST):
		# a new search has been initiated
		sessionVar.append(dict())

		(searchAp, searchCcEpi, searchLocs, searchIsln, searchProj) = loadRequestSearchVars_detail(request.POST)

		sessionVar[0]['json_apSearchTerms'] = searchAp
		sessionVar[0]['json_ccEpiSearchTerms'] = searchCcEpi
		sessionVar[0]['json_location'] = searchLocs
		sessionVar[0]['json_isolation'] = searchIsln
		sessionVar[0]['json_project'] = searchProj

		sessionVar[0]['pageType'] = cl.SearchIsolateDetail

	else:
		raise Http404('Search variables not found!')

	json_sessionVar = json.dumps(sessionVar, cls=DjangoJSONEncoder)
	request.session['sessionVar'] = json_sessionVar


	# print("updated version")
	# print (searchVar)
	###########################

	arr_ap = []; arr_ccEpi = []; arr_iso = []; arr_isln = []; arr_loc = [];
	if searchAp:
		arr_ap = [searchAp]
	if searchCcEpi:
		arr_ccEpi = [searchCcEpi]
	if searchLocs:
		arr_loc = [searchLocs]
	if searchIsln:
		arr_isln = [searchIsln]
	if searchProj:
		projectId = Project.objects.get(identifier=searchProj['project']).id
		if not routeToRightFnAuth.isProjectByUser(projectId, request.user.username):
			raise Http404("Error you dont have access to page. Go back.")
		searchProj['project'] = projectId
		arr_iso = [searchProj]


	if request.user.is_authenticated:

		(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn(arr_ap, arr_ccEpi, [], arr_loc, arr_isln, arr_iso, pageNumToGet, maxIsolatesPerPage, request.user.username, True, orderBy, dir)
	else:

		(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn([searchAp], [searchCcEpi], [], [searchLocs], [searchIsln], [], pageNumToGet, maxIsolatesPerPage, None, None, orderBy, dir)




	mergedIds = det.convertToJson_dict(dict_mergedIds)


	if isCsv:
		outstring = makeCsv(isolates,request.user.is_authenticated)
		return HttpResponse(outstring)
	else:
		jsonIso = det.convertToJson(isolates)

		outdata = {"isolates": jsonIso, "isoCount": isoCount, "pageInfo": dict_pageInfo, "isAp": isAp, 'isDst':isDst, 'isMgtColor': isMgtColor, "colIsoId": c.IsolateId, "isoInfo": isoInfo, "apInfo": apHeader, "ccInfo": ccHeader, "mgtInfo": mgtInfo, "epiInfo": epiInfo, "locInfo": locInfo, "islnInfo": islnInfo, "mergedIds": mergedIds}

		return render(request, 'Salmonella/isolateTable.html', outdata)


def loadRequestSearchVars_detail(requestVar):
	searchAp = json.loads(requestVar['json_apSearchTerms'])
	searchCcEpi = json.loads(requestVar['json_ccEpiSearchTerms'])
	searchLocs = json.loads(requestVar['json_location'])
	searchIsln = json.loads(requestVar['json_isolation'])
	searchProj = json.loads(requestVar['json_project'])

	return (searchAp, searchCcEpi, searchLocs, searchIsln, searchProj)
