from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def isSame(context, url1):
	request = context['request']
	if request.path == url1:
	    return "disabled"


	return ""