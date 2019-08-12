from django import forms
from Salmonella.models import Location, Isolate, Isolation, Project, User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from Salmonella.views.FuncsAuxAndDb import queryDb as q
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from . import isolateForms_CreateEdit as isolateForms


def page(request):

	if len(request.POST) == 0:

		projs = q.getUserProjectIds(request.user.username)
		print(projs)
		if len(projs) == 0: # user has not created any projects for this organism # check for url hacking.
			# then redirect to force them to create project.

			return redirect('/Salmonella/create-project')


		form_loc = isolateForms.LocationForm()
		form_isln = isolateForms.IsolationForm()

		if len(request.GET) > 0:
			# print("prefil single projectid")

			if not (int(request.GET.get('project')) in projs): # if requested project is not in user's projects
				raise PermissionDenied("Error: you are trying to add an isolate to a project that is not yours.")

			form_iso = isolateForms.IsolateForm(request.user, initial={'project': Project.objects.get(id=request.GET.get('project'))})

		else:
			print("get all users project ids")
			form_iso = isolateForms.IsolateForm(request.user)


	if len(request.POST) > 0:
		# print (request.POST)
		# print (" new isolate info submitted, to check and return errors, or if all good, save!")

		# print(request.POST)

		# load forms with user supplied data
		form_iso = isolateForms.IsolateForm(request.user, request.POST, request.FILES)
		form_isln = isolateForms.IsolationForm(request.POST)
		form_loc = isolateForms.LocationForm(request.POST)


		if  not form_iso.is_valid() or not form_loc.is_valid() or not form_isln.is_valid():
			# form_iso.is_valid() should also check that one of (file_f, file_r) or (file_alleles) are supplied.

			return render(request, 'Salmonella/isolateCreate.html', {'form_loc': form_loc, 'form_iso': form_iso, 'form_isln': form_isln})

		else:
			# handle save() for each form.
			locObj = form_loc.save()
			islnObj = form_isln.save()

			isolateObj = form_iso.save(commit=False)

			if "file_alleles" in request.FILES:
				isolateObj.server_status = 'V'
			elif "file_forward" in request.FILES and "file_reverse" in request.FILES:
				isolateObj.server_status = 'U'





			if locObj:
				isolateObj.location = locObj

			if islnObj:
				isolateObj.isolation = islnObj

			isolateObj.save()

			return HttpResponseRedirect(reverse('Salmonella:isolate_detail', kwargs={'pk': isolateObj.id}))

			# isoPk = saveIsolate(locObj, islnObj)
			# pass

	return render(request, 'Salmonella/isolateCreate.html', {'form_loc': form_loc, 'form_iso': form_iso, 'form_isln': form_isln})
