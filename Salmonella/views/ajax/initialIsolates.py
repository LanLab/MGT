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
from Salmonella.views.FuncsAuxAndDb import sessionFns as ses
from Salmonella.views.FuncsAuxAndDb import queryDb as q
from Salmonella.views.FuncsAuxAndDb.makeCsvString import makeCsv
from Salmonella.views.FuncsAuxAndDb import ownPaginator as ownPaginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from types import MethodType
from django.http import Http404

@csrf_exempt
def page(request):

	sessionVar = list()

	pageNumToGet = 1
	orderBy = None
	dir = None

	isCsv = False;
	maxIsolatesPerPage = c.TOTAL_ISO_PER_PAGE


	if (('orderBy' in request.POST and len(request.POST['orderBy']) > 0) or ('pageNumToGet' in request.POST and len(request.POST['pageNumToGet']) > 0)) or ('isCsv' in request.POST and request.POST['isCsv'] == 'true'):
		# session var should be reused and updated
		sessionVar_json = request.session['sessionVar']
		sessionVar = json.loads(sessionVar_json)

		if sessionVar[0]['pageType'] != cl.InitialIsolates:
			raise Http404()


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


	else:
		# load all public data
		sessionVar.append(dict())
		sessionVar[0]['pageType'] = cl.InitialIsolates



	json_sessionVar = json.dumps(sessionVar, cls=DjangoJSONEncoder)
	request.session['sessionVar'] = json_sessionVar



	############################

	isoCount = 0
	dict_pageInfo = dict()
	isolates = []


	if request.user.is_authenticated:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPv)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)

		(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn([], [], [], [], [], [], pageNumToGet, maxIsolatesPerPage,  request.user.username, None, orderBy, dir)



	else:
		isoInfo = det.convertToJson(c.IsolateHeaderPu)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		mgtInfo = det.convertToJson(c.MgtColsPu)
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPu)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPu)

		(isoCount, isolates, dict_pageInfo, dict_mergedIds) = routeToRightFnAuth.getIsolatesFromRightFn([], [], [], [], [], [], pageNumToGet, maxIsolatesPerPage, None, None, orderBy, dir)


	isAp = True; isDst = False; isMgtColor = True;
	if 'isAp' in request.POST and request.POST['isAp'] == "false":
		isAp = False
	if 'isDst' in request.POST and request.POST['isDst'] == 'true':
		isDst = True
	if 'isMgtColor' in request.POST and request.POST['isMgtColor'] == 'false':
		isMgtColor = False

	# print ("is mgtcolor is " + str(isMgtColor) + " ... " + request.POST['isAp'])

	# print(' GETTING TO THE END!')
	if isCsv:
		outstring = makeCsv(isolates,request.user.is_authenticated)
		return HttpResponse(outstring)
	else:
		isolatesjson = det.convertToJson(isolates)

		return render(request, 'Salmonella/isolateTable.html', {"isolates": isolatesjson, "isoCount": isoCount, "pageInfo": dict_pageInfo, "isAp": isAp, "colIsoId": c.IsolateId, "isoInfo": isoInfo, "apInfo": apHeader, "ccInfo": ccHeader, "mgtInfo": mgtInfo, "epiInfo": epiInfo, "locInfo": locInfo, "islnInfo": islnInfo, "isDst": isDst, "isMgtColor": isMgtColor})
