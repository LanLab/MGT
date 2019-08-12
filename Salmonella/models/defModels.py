from django.db import models
from Mgt.settings import MEDIA_ROOT
from Mgt.settings import SUBDIR_REFERENCES
from Mgt.settings import SUBDIR_ALLELES
# Create your models here.


def validate_isAllele(value):
	if not Allele.objects.filter(id=value).exists():
		raise ValidationError(
		('%(value)s is not an id in the allele database'),
		params={'value': value},
		)


class Reference(models.Model):
	identifier = models.CharField(max_length=100, primary_key=True, verbose_name='Organism short name')
	organism = models.CharField(max_length=100, verbose_name='Organism scientific name')
	description = models.TextField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.identifier

class Chromosome(models.Model):
	number = models.IntegerField(primary_key=True)
	reference = models.ForeignKey(Reference, on_delete="PROTECT")
	file_location = models.FileField(upload_to=SUBDIR_REFERENCES)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.reference.identifier + ", " + str(self.number)


class Locus(models.Model):
	identifier = models.CharField(max_length=100, primary_key=True)
	start_location = models.IntegerField()
	end_location = models.IntegerField()

	orientation_type_choices = (
		('+', 'Forward'),
		('-', 'Reverse'))

	orientation = models.CharField(
		max_length=1,
		choices=orientation_type_choices
	)

	locus_type_choices = (  # should this be a field?
		('GN', 'Gene'),
		('PS', 'Pseudogene'),
		('IG', 'Intergenic'),
		('PR', 'Promoter'),
		('OT', 'Other')
	)
	locus_type = models.CharField(
		max_length=2,
		choices=locus_type_choices,
		blank=True,
		null=True,
	)

	chromosome = models.ForeignKey(
		'Chromosome', on_delete=models.PROTECT, db_index=False)

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.identifier)


class Snp(models.Model):
	position = models.IntegerField(verbose_name='with regards to allele seq.')
	aa_choices = (
		('A', 'Adenine'),
		('C', 'Cytosine'),
		('G', 'Guanine'),
		('T', 'Thymine'),
		('N', 'Unidentified'),
	)
	original_aa = models.CharField(
		max_length=1,
		choices=aa_choices,
	)
	altered_aa = models.CharField(
		max_length=1,
		choices=aa_choices,
	)
	# FK to sequence from this table or the opposite ?

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = (("position", "original_aa", "altered_aa"),)

	def __str__(self):
		return "%s, %s -> %s" % (str(self.position), str(self.original_aa), str(self.altered_aa))


class Allele(models.Model):
	identifier = models.CharField(max_length=50) # FIXED: not integer field to accomodate "_" in the naming.
	locus = models.ForeignKey('Locus', on_delete=models.PROTECT)

	# make id and locus unique
	length = models.IntegerField()
	hasSnp = models.BooleanField()

	snps = models.ManyToManyField(Snp)

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	file_location = models.FileField(upload_to=SUBDIR_ALLELES, max_length=500)
	class Meta:
		unique_together = (("identifier", "locus"),)

	def __str__(self):
		return str(self.locus.identifier) + ", " + str(self.identifier)

"""
class Sequence(models.Model):
	# FK to sequence from this table or the opposite ?
	allele = models.OneToOneField(
		'Allele', on_delete=models.CASCADE, primary_key=True)
	file_location = models.FileField()

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "%s, %s" % (str(self.allele.locus.identifier), str(self.allele.identifier))
"""


class Scheme(models.Model):
	identifier = models.CharField(max_length=50, primary_key=True)

	loci = models.ManyToManyField(Locus)

	uncertainty_threshold = models.IntegerField(verbose_name='limit on number of genes == 0')

	# order_num = models.IntegerField(unique=True, verbose_name='order of computation')

	description = models.TextField(null=True, blank=True)

	display_name = models.CharField(max_length=50)

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.identifier

class Tables_ap(models.Model):
	scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT)
	table_num = models.IntegerField() # table number 0 for each scheme will contain the cc info and autoId Field
	table_name = models.CharField(max_length=50, unique=True)
	display_order = models.IntegerField(blank=True, null=True) # only required for the 0 numbered tables.
	display_name = models.CharField(max_length=50)

class Tables_cc(models.Model):
	scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT)
	table_name = models.CharField(max_length=50)
	display_table = models.IntegerField(verbose_name="table to display it in")
	display_order = models.IntegerField(verbose_name="order of display in display_table")
	display_name = models.CharField(max_length=50)

	class Meta:
		unique_together = (("scheme", "display_table", "display_order"),)

"""
class Clonal_complex(models.Model):
	scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT)

	identifier = models.IntegerField() # primary_key this?
	curr_id = models.ForeignKey('self', on_delete='PROTECT', blank=True, null=True)
	merge_timestamp = models.DateTimeField(auto_now=True) # only update if curr_id is updated.

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = (("scheme", "identifier"),)

	def __str__(self):
		if self.curr_id:
			return "%s, %s: %s, %s" % (self.scheme.identifier, str(self.identifier), str(self.curr_id.identifier), str(self.merge_timestamp))
		else:
			return "%s, %s: %s, %s" % (self.scheme.identifier, str(self.identifier), "-", str(self.merge_timestamp))



class Allelic_profile(models.Model):
	st = models.IntegerField()
	dst = models.IntegerField()

	scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT)

	alleles = models.ManyToManyField(Allele)
	clonal_complex = models.ForeignKey(
		Clonal_complex, on_delete=models.PROTECT, null=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = (("scheme", "st", "dst"),)

	def __str__(self):
		return "%s: %s, %s" % (self.scheme.identifier, str(self.st), str(self.dst))


class Scheme_group(models.Model):
	identifier = models.CharField(max_length=50, primary_key=True)
	schemes = models.ManyToManyField(Scheme, through='SchemesInGroups')
	description = models.TextField(null=True, blank=True)


	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.identifier


class SchemesInGroups(models.Model):
	scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT)
	group = models.ForeignKey(Scheme_group, on_delete=models.PROTECT)
	order_num = models.IntegerField(
		verbose_name='order # of scheme in scheme_group')

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = (("scheme", "group"))

	def __str__(self):
		return "%s, %s" % (self.group, self.scheme)
"""
"""
class Hst(models.Model):
	scheme_group = models.ForeignKey('Scheme_group', on_delete=models.PROTECT)
	allelic_profiles = models.ManyToManyField(
		Allelic_profile)

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "%s: %s" % (self.scheme_group.identifier, self.id)
"""
