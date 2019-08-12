from django.shortcuts import render
from Salmonella.models import Isolate, Reference, Tables_ap
from Salmonella.views.FuncsAuxAndDb import getHeaders

# Create your views here.


def page(request):

	try:
		isoCount = Isolate.objects.filter(privacy_status="PU").count()
	except:
		isoCount = 0

	try:
		isoCount_assigned = Isolate.objects.filter(privacy_status="PU", server_status="C", assignment_status="A").count()
	except:
		isoCount_assigned = 0

	try:
		organism = Reference.objects.all()[0].organism # getting the first one's name
		request.session['organism'] = organism
	except:
		request.session['organism'] = "Organism"

	try:
		mgts = getHeaders.getApHeaderAsJson()
	except:
		mgts = None


	return render(request, "Salmonella/index.html", {"isoCount": isoCount, "isoCount_assigned": isoCount_assigned, "mgts": mgts})
