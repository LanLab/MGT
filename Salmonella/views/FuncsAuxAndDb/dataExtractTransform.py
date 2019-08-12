from django.db.models import Q
import operator
from django.core.serializers.json import DjangoJSONEncoder
import json
import ast


def getEpiDictFromReq(epi_colName, epiVal):
	dict_epi = dict()

	# epi col names
	epiCurr_colName = epi_colName + "_curr"

	# epi dict
	dict_epi[epi_colName] = epiVal
	dict_epi[epiCurr_colName] = epiVal

	return dict_epi


def getApDictFromReq(ap_tn, st, dst):
	dict_ap = dict()

	# ap dict
	col_st = ap_tn + "_st"
	col_dst = None
	if dst:
		col_dst = ap_tn + "_dst"
		dict_ap[col_dst] = dst

	dict_ap[col_st] = st

	return dict_ap

def getOrQ(dict_):
	orQ = Q()

	for item in dict_:
		orQ |= Q(**{item:dict_[item]})

	return (orQ)

def getOrQ_cc(key, val):
	orQ = Q()

	orQ = Q()
	orQ |= Q(**{key:val})
	orQ |= Q(**{key+"_merge":val})

	return (orQ)


def makeAndOfOrQs(dict_mergedIds):
	andOfOrQs = Q()

	for tn in dict_mergedIds:
		orQ = Q()
		for val in dict_mergedIds[tn]:
			orQ |= Q(**{tn:val})
			orQ |= Q(**{tn+"_merge":val})

			# print(orQ)
		andOfOrQs &= orQ

	return andOfOrQs


def getAndQ(dict_):
	andQ = Q()

	for item in dict_:
		andQ &= Q(**{item:dict_[item]})

	return (andQ)

def addToAndQFromList(andQ, list_):
	for dict_ in list_:
		for key in dict_:
			andQ &= Q(**{key:dict_[key]})

	return andQ


def addOrToOrQFromList(orQ, tn, list_):
	for val in list_:
		# for key in dict_:
			tmpQ = Q()

			tmpQ |= Q(**{tn:val})
			tmpQ |= Q(**{tn+"_merge":val})

			orQ |= tmpQ

	return orQ

def addOrToAndQFromList(andQ, list_):
	for dict_ in list_:
		for key in dict_:
			orQ = Q()
			orQ |= Q(**{key:dict_[key]})
			orQ |= Q(**{key+"_merge":dict_[key]})

			andQ &= orQ

	return andQ

def addToAndQICntnsFromList(andQ, list_):
	for dict_ in list_:
		for key in dict_:
			theStr = key + "__icontains"
			andQ &= Q(**{theStr:dict_[key]})

	return andQ

def convertToJson(list_iso):
	return json.dumps(list(list_iso), cls=DjangoJSONEncoder)

def convertToJson_dict(dict_):
	dumped = json.dumps(dict_)
	dumped = dumped.replace("\'", '\"')
	return dumped
	# return ast.literal_eval(dummped)
