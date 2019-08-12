from django.views.generic import CreateView
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django import forms
from django.http import HttpResponse, HttpResponseServerError
from Salmonella.models import Isolate, View_apcc, Tables_ap
from django.forms.models import model_to_dict
# from . import hgt_db_functions
from operator import attrgetter
from itertools import chain
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from Salmonella.views.FuncsAuxAndDb import getHeaders
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import constants as c
from itertools import *
from django.db import connections

def getApColsForDisplay(db_cols, apCols, prependStart, prependEnd):
	print (db_cols)
	list_colsToDisp = list()
	list_dispNames = list()

	for apTn in apCols:
		print (apTn)

		st = apTn['table_name'] + "_st"
		dst = apTn['table_name'] + "_dst"

		if st in db_cols:
			list_colsToDisp.append(db_cols.index(st))
			list_dispNames.append(apTn['scheme__display_name'])

		if dst in db_cols:
			list_colsToDisp.append(db_cols.index(dst))


	for i in range(prependEnd, prependStart-1, -1):
		list_colsToDisp.insert(0, i)
		list_dispNames.insert(0, db_cols[i])


	print (list_dispNames)

	# print (list_colsToDisp)
	return (list_colsToDisp, list_dispNames)

ISOLATE_START = 0
ISOLATE_END = 1

def page(request):

	if request.user.is_authenticated:
		isoInfo = det.convertToJson(c.IsolateHeaderPv)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPv)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPv)
	else:
		isoInfo = det.convertToJson(c.IsolateHeaderPu)
		apHeader = getHeaders.getApHeaderAsJson()
		ccHeader = getHeaders.getCcHeaderAsJson()
		epiInfo = getHeaders.getEpiHeaderAsJson()
		locInfo = det.convertToJson(c.IsoMetaLocInfoPu)
		islnInfo = det.convertToJson(c.IsoMetaIslnInfoPu)


	return render(request, 'Salmonella/isolateList.html', {"isoHeader": isoInfo, "apHeader": apHeader, "ccHeader": ccHeader, "epiHeader": epiInfo, "locHeader": locInfo, "islnHeader": islnInfo})
