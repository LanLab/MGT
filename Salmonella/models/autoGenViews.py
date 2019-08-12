from django.db import models
# from .defModels import *
from .autoGenAps import *
from .autoGenCcs import *


class View_apcc(models.Model):

	class Meta:
		managed = False
		db_table = "Salmonella_view_apcc"


"""
class View_apcc(models.Model):

	class Meta:
		managed = False
		# db_table = "Salmonella_view_apcc"
"""
