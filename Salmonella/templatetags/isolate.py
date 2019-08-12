from django import template

register = template.Library()

@register.filter
def getFileName(value):
	tmp = str(value).split("/")
	return tmp[len(tmp)-1]