from django import template

import json
import os

register = template.Library()

@register.filter
def getValue(dict_, key):
	print(key)
	return dict_[key]

@register.filter
def getApVal(qsObj, key):
	return getattr(qsObj, key)

@register.filter
def hasKey(qsObj, key):
	return hasattr(qsObj, key)


@register.filter
def getValForHst(qsObj, colName):

	val = getattr(qsObj, colName)
	if not val:
		return ""

	if val.dst == 0:
		return val.st
	return val


@register.filter
def getDispForAp(qsObj, tn):

	val = getattr(qsObj, tn)
	if not val:
		return ""

	val = getattr(qsObj, tn + "_st")
	dst = getattr(qsObj, tn + "_dst")

	if dst and dst != 0:
		val = str(val) + "." + str(dst)

	return val


@register.filter
def getDispForCc(obj, tn):
	pass


@register.filter
def loadjson(data):
	return json.loads(data)


@register.filter(name='get_class')
def get_class(value):
	return value.__class__.__name__


@register.filter
def getListValByIdx(list_, idx):
	return list_[idx]


@register.filter
def filenameOnly(pathAndFile):
	return os.path.basename(pathAndFile)
