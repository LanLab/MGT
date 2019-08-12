from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from Salmonella.views.FuncsAuxAndDb import getHeaders, routeToRightFnAuth, getPoolOfCcMergeIds
from Salmonella.models import View_apcc
from itertools import *
from django.db import connections
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import queryDb
from Salmonella.views.FuncsAuxAndDb.makeCsvString import makeCsv
from Salmonella.views.FuncsAuxAndDb import constants as c
from Salmonella.views.FuncsAuxAndDb import constants_local as cl
from Salmonella.views.FuncsAuxAndDb import getPoolOfCcMergeIds as getCcMergeIdsList
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from types import MethodType
from django.db.models import Q
import re
from Salmonella.views.FuncsAuxAndDb import sessionFns as ses

@csrf_exempt
def page(request):

	sessionVar = list()

	pageNumToGet = 1
	orderBy = None
	dir = None

	isCsv = False;
	maxIsolatesPerPage = c.TOTAL_ISO_PER_PAGE


	arr_ap = []; arr_cc = []; arr_epi = []; arr_iso = []; arr_isln = []; arr_loc = [];


	if (('orderBy' in request.POST and len(request.POST['orderBy']) > 0) or ('pageNumToGet' in request.POST and len(request.POST['pageNumToGet']) > 0)) or ('isCsv' in request.POST and request.POST['isCsv'] == 'true'):

		# session var should be reused and updated
		sessionVar_json = request.session['sessionVar']
		sessionVar = json.loads(sessionVar_json)

		if sessionVar[0]['pageType'] != cl.SearchIsolateList:
			raise Http404()

		(arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc) = ses.loadSessionSearchVars(sessionVar)


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



	elif ses.isASearchPresent(request.POST):
		sessionVar.append(dict())

		(arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc) = ses.loadRequestSearchVars(request.POST)

		sessionVar[0]['arrAp'] = arr_ap
		sessionVar[0]['arrCc'] = arr_cc
		sessionVar[0]['arrEpi'] = arr_epi
		sessionVar[0]['arrIso'] = arr_iso
		sessionVar[0]['arrIsln'] = arr_isln
		sessionVar[0]['arrLoc'] = arr_loc

		sessionVar[0]['pageType'] = cl.SearchIsolateList
	else:
		raise Http404('No search variables found')



	json_sessionVar = json.dumps(sessionVar, cls=DjangoJSONEncoder)
	request.session['sessionVar'] = json_sessionVar


	########################


	isAp = True; isDst = False; isMgtColor = True;
	if 'isAp' in request.POST and request.POST['isAp'] == "false":
		isAp = False
	if 'isDst' in request.POST and request.POST['isDst'] == 'true':
		isDst = True
	if 'isMgtColor' in request.POST and request.POST['isMgtColor'] == 'false':
		isMgtColor = False


	# HEADERS
	if request.user.is_authenticated:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPv)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)

		(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn(arr_ap, arr_cc, arr_epi, arr_loc, arr_isln, arr_iso, pageNumToGet, maxIsolatesPerPage, request.user.username, False, orderBy, dir)

	else:
		isoInfo = det.convertToJson(c.IsolateHeaderPu)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPu)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPu)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPu)

		# print("is not authenticated")


		(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn(arr_ap, arr_cc, arr_epi, arr_loc, arr_isln, arr_iso, pageNumToGet, maxIsolatesPerPage, None, False, orderBy, dir)




	mergedIds = det.convertToJson_dict(dict_mergedIds)

	# print(dict_mergedIds)

	if isCsv:
		outstring = makeCsv(isolates,request.user.is_authenticated)
		return HttpResponse(outstring)
	else:
		jsonIso = det.convertToJson(isolates)

		return render(request, 'Salmonella/isolateTable.html', {"isolates": jsonIso, "isoCount": isoCount, "pageInfo": dict_pageInfo, "isAp": isAp, 'isDst': isDst, 'isMgtColor': isMgtColor, "colIsoId": c.IsolateId, "isoInfo": isoInfo, "apInfo": apHeader, "ccInfo": ccHeader, "mgtInfo": mgtInfo, "epiInfo": epiInfo, "locInfo": locInfo, "islnInfo": islnInfo, "mergedIds" : mergedIds})
