from django import forms
from Salmonella.models import Location, Isolate, Isolation, Project, User
from Salmonella.views.FuncsAuxAndDb import defaults

class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ['continent', 'country', 'state', 'postcode']
		widgets = {
			'continent': forms.Select(attrs={'required':'true'}),
			'country': forms.Select(attrs={'required':'true'}),
		}

	def save(self):
		if isAllEmpty([self.instance.continent, self.instance.country, self.instance.state, self.instance.postcode]):
			return None

		locObj = getLocIfExists(self.instance.continent, self.instance.country, self.instance.state, self.instance.postcode)

		if not locObj:
			locObj = super().save(commit=True)

		return locObj


def isAllEmpty(list_):
	for val in list_:
		if val:
			return False

	return True


def getLocIfExists(continent, country, state, postcode):
	locObjs = Location.objects.filter(continent=continent, country=country, state=state, postcode=postcode)

	if len(locObjs) > 0: # if object already exists
		return locObjs.get()

	return None

def getIslnIfExists(source, type, host, disease, date, year):
	islnObjs = Isolation.objects.filter(source=source, type=type, host=host, disease=disease, date=date, year=year)

	if len(islnObjs) > 0:
		return islnObjs.get()

	return None



class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)



class IsolationForm(forms.ModelForm):

	class Meta:
		model = Isolation
		fields = ['source', 'type', 'host', 'disease', 'date', 'year']
		widgets = {
			'date': forms.DateInput(attrs={'class':'datepicker'}),
			'year': forms.Select(attrs={'required':'true'}),
			'source': ListTextWidget(data_list=Isolation.objects.values_list('source').distinct(), name='source_list'),
			'host': ListTextWidget(data_list=Isolation.objects.values_list('host').distinct(), name='host_list'),
			'type': ListTextWidget(data_list=Isolation.objects.values_list('type').distinct(), name='type_list'),
			'disease': ListTextWidget(data_list=Isolation.objects.values_list('disease').distinct(), name='disease_list'),

		}


	# check date & year
	def clean(self):
		cleaned_data = super().clean()

		if 'date' in cleaned_data and 'year' in cleaned_data:
			print ("both are supplied here")
			print(cleaned_data)

			if cleaned_data['date'] != None and cleaned_data['date'].year != cleaned_data['year']:
				raise forms.ValidationError('Error: Date\'s year and Year are not the same. You can simply supply date, and year will be extracted.')

		# print (cleaned_data)

	def save(self):
		if isAllEmpty([self.instance.source, self.instance.type, self.instance.host, self.instance.disease, self.instance.date, self.instance.year]):
			return None

		if self.instance.date and not self.instance.year:
			self.instance.year = self.instance.date.year

		islnObj = getIslnIfExists(self.instance.source, self.instance.type, self.instance.host, self.instance.disease, self.instance.date, self.instance.year)

		if not islnObj:
			islnObj = super().save(commit=True)

		return islnObj



class IsolateForm(forms.ModelForm):

	class Meta:
		model = Isolate
		fields = ['identifier', 'privacy_status', 'file_forward', 'file_reverse', 'file_alleles', 'project']


	def __init__(self, user, *args, **kwargs):
		super(IsolateForm, self).__init__(*args, **kwargs)

		self.fields['project'].queryset = Project.objects.filter(user=User.objects.get(userId=user))

	def clean(self):
		cleaned_data = super().clean()
		# print(cleaned_data)

		# if no files are provided
		if cleaned_data['file_forward'] == None and cleaned_data['file_reverse'] == None and cleaned_data['file_alleles'] == None:
			raise forms.ValidationError('Error: You must supply 2 illumina reads files (forward and reverse), or alleles, extracted using the MGT pipeline.')

		# if only one of the 2 illumina reads files is provided.
		if (cleaned_data['file_forward'] or cleaned_data['file_reverse']) and not (cleaned_data['file_forward'] and cleaned_data['file_reverse']):
			raise forms.ValidationError('Error: You must supply both illumina reads files.')

		# print (cleaned_data)
