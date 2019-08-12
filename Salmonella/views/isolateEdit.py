from django import forms
from Salmonella.models import Location, Isolate, Isolation, Project, User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from Salmonella.views.FuncsAuxAndDb import queryDb as q
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from . import isolateForms_CreateEdit as isolateForms

def page(request, pk):

	# CHECK: user has permission; if False <- send permission denied.
	if not has_permission(pk, request.user.username):
		raise PermissionDenied("Error: you dont have permission to edit this isolate.")

	isoObj = Isolate.objects.get(id=pk)

	if len(request.POST) == 0:


		form_iso = IsolateForm(request.user, instance=isoObj)
		form_loc = None
		form_isln = None

		if isoObj.location:
			form_loc = isolateForms.LocationForm(instance=Location.objects.get(id=isoObj.location.id))
		else:
			form_loc = isolateForms.LocationForm()

		if isoObj.isolation:
			form_isln = isolateForms.IsolationForm(instance=Isolation.objects.get(id=isoObj.isolation.id))
		else:
			form_isln = isolateForms.IsolationForm()



		return render(request, 'Salmonella/isolateEdit.html', {'form_iso': form_iso, 'form_loc': form_loc, 'form_isln': form_isln})

	if len(request.POST) > 0:
		form_iso = IsolateForm(request.user, request.POST, instance=isoObj)

		if not isoObj.location:
			form_loc = isolateForms.LocationForm(request.POST)
		else:
			form_loc = isolateForms.LocationForm(request.POST, instance=Location.objects.get(id=isoObj.location.id))

		if not isoObj.isolation:
			form_isln = isolateForms.IsolationForm(request.POST)
		else:
			form_isln = isolateForms.IsolationForm(request.POST, instance=Isolation.objects.get(id=isoObj.isolation.id))

		if not form_iso.is_valid() or not form_loc.is_valid() or not form_isln.is_valid():

			return render(request, 'Salmonella/isolateCreate.html', {'form_loc': form_loc, 'form_iso': form_iso, 'form_isln': form_isln})

		else:
			locObj = form_loc.save()
			islnObj = form_isln.save()

			isolateObj = form_iso.save(commit=False)
			# isolateObj.server_status = 'U' - dont update server status here.

			if locObj:
				isolateObj.location = locObj

			if islnObj:
				isolateObj.isolation = islnObj

			isolateObj.save()

		# print("process results: if any errors, resend form with errors; if all good, then reponse redirect")

	return HttpResponseRedirect(reverse('Salmonella:isolate_detail', kwargs={'pk': pk}))

def has_permission(pk, username):
	if User.objects.filter(userId=username).count() > 0: # if user exists
		if Isolate.objects.get(id=pk).project.user == User.objects.get(userId=username):
			return True

	return False

########################### ModelForms

class IsolateForm(forms.ModelForm):

	class Meta:
		model = Isolate
		fields = ['identifier', 'privacy_status', 'project']

	def __init__(self, user, *args, **kwargs):
		super(IsolateForm, self).__init__(*args, **kwargs)

		self.fields['project'].queryset = Project.objects.filter(user=User.objects.get(userId=user))
