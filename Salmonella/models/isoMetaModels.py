from django.db import models
from django_countries import countries
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class Location(models.Model):
	continent_choices = (
		('Africa', 'Africa'),
		('Antarctica', 'Antarctica'),
		('Oceania', 'Oceania'),
		('North America', 'North America'),
		('South America', 'South America'),
		('Europe', 'Europe'),
		('Asia', 'Asia'),
	)

	continent = models.CharField(max_length=15, choices=continent_choices, blank=True, null=True)

	countryAbrev = list(countries)
	countryCountry = [(x[1],x[1]) for x in countryAbrev]
	country = models.CharField(max_length=75, choices=countryCountry, blank=True, null=True)

	# country = CountryField(country_dict=True, blank=True, null=True)
	state = models.CharField(max_length=100, verbose_name="State or sub country", blank=True, null=True)
	postcode = models.IntegerField(blank=True, null=True)

	class Meta:
		unique_together = (("continent", "country", "state", "postcode"),)



def year_choices():
    return [(r,r) for r in range(datetime.date.today().year, 1900, -1)]

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Isolation(models.Model):

	# source = models.CharField(max_length=100, blank=True, null=True)
	source = models.CharField(max_length=100, blank=True, null=True)
	type = models.CharField(max_length=50, blank=True, null=True)
	#host = models.CharField(max_length=100, blank=True, null=True)
	host = models.CharField(max_length=100, blank=True, null=True)
	disease = models.CharField(max_length=120, blank=True, null=True, verbose_name="Host disease")
	# comments = models.TextField(blank=True, null=True)
	date = models.DateField(blank=True, null=True, verbose_name="Collection date")


	# year = models.IntegerField(blank=True, null=True, verbose_name="Collection year")
	year = models.IntegerField(choices=year_choices(), blank=True, null=True, verbose_name="Collection year")

	class Meta:
		unique_together = (("source", "type", "host", "disease", "date", "year"),)




class ExternalFks(models.Model):
	fkId = models.CharField(max_length=50)
	url = models.CharField(max_length=140, blank=True, null=True)
	name = models.CharField(max_length=50, verbose_name="Web resource name")

	class Meta:
		unique_together = (("fkId", "name"),)
