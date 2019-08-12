import sys

def getAllCcsWithMergeId(ccTableObj, mergeId):
	qs_ccObjs = None

	try:
		qs_ccObjs = ccTableObj.objects.filter(merge_id=mergeId)

	except:
		sys.stderr.write("Error: unable to get ccObjs with merge_id " + str(mergeId) + "\n")

	return qs_ccObjs


def getApTns(appClass, tableNum):
	qs_tns = None

	try:
		qs_tns = appClass.models.Tables_ap.objects.filter(table_num=tableNum).distinct().order_by('display_order')
	except:
		sys.stderr.write("Error: unable to get ap tns with tableNums " + str(tableNum) + "\n")
		raise

	return qs_tns

def getCcTns(appClass):
	qs_tns = None

	try:
		qs_tns = appClass.models.Tables_cc.objects.all().distinct().order_by('display_table', 'display_order')
	except:
		sys.stderr.write("Error: unable to get all cc tns \n")
		raise

	return qs_tns

def getDbFk(appClass, fkId, dbName):
	qs_fk = None

	try:
		qs_fk = appClass.models.ExternalFks.objects.filter(fkId=fkId, name=dbName).get()

	except:
		sys.stderr.write("Note: no metadata fkObj found " + str(fkId) + " " + str(dbName) + '\n')

	return qs_fk



def getIsolation(appClass, source, type, host, hostDisease, date, year):
	qs_isolation = None

	try:
		qs_isolation = appClass.models.Isolation.objects.filter(source=source, type=type, host=host, disease=hostDisease, date=date, year=year).get()


	except:
		sys.stderr.write("Note, no isolation found " + str(source) + " " + str(type) + " " + str(host) + " " + str(hostDisease) + " " + str(date) + '\n')

	return qs_isolation


def getLocation(appClass, continent, country, state, postcode):
	qs_loc = None

	try:
		qs_loc = appClass.models.Location.objects.filter(continent=continent, country=country, state=state, postcode=postcode).get()
		return qs_loc

	except:
		sys.stderr.write("Note, no loc found " + str(continent) + " " + str(country) + " " + str(state) + " " + str(postcode) + '\n')


def getCcTn(appClass, tableNum, displayOrd):
	qs_tn = None

	try:
		qs_tn = appClass.models.Tables_cc.objects.filter(display_table=tableNum, display_order=displayOrd).get()
		return qs_tn

	except:
		sys.stderr.write("Note: no cc table for tableNum:" + tableNum + " displayOrder:" + displayOrd +'\n')
		# raise



def getCcTnsForScheme(appClass, schObj):
	qs_tns = None

	try:
		qs_tns = appClass.models.Tables_cc.objects.filter(scheme=schObj).distinct('table_name')

	except:
		sys.stderr.write("Note: no ccs for " + schObj.identifier)
		# raise

	return qs_tns


def getCcTnForScheme(appClass, schName, tableNum, displayOrd):
	qs_tn = None

	try:
		qs_tn = appClass.models.Tables_cc.objects.filter(scheme=schName, display_table=tableNum, display_order=displayOrd).get()
		return qs_tn

	except:
		sys.stderr.write("Note: no cc table for Scheme:" + schName + " tableNum:" + tableNum + " displayOrder:" + displayOrd +'\n')
		# raise


def getHst(appClass, dict_hgtQry, shouldExit):

	hgtObj = None

	try:
		hgtObj = appClass.models.Mgt.objects.get(**dict_hgtQry)


	except:
		sys.stderr.write("Note: unable to retrive hgt obj from db\n")

		if shouldExit == True:
			raise

	return hgtObj

def getProject(appClass, username, identifier, shouldExit):
	projObj = None

	try:
		projObj = appClass.models.Project.objects.filter(user=username, identifier=identifier).get()
		return projObj
	except:
		sys.stderr.write("Note: unable to get project with id " + identifier + " for user " + username  + '\n')

		if shouldExit == True:
			raise


def getIsolate(appClass, projectName, isolateName):

	isolateObj = None

	try:
		isolateObj = appClass.models.Isolate.objects.get(project=projectName, identifier=isolateName)

	except:
		sys.stderr.write("Error: unable to get isolate " + str(isolateName) + " for project " + str(projectName) + " from table \n")
		raise

	return isolateObj



def getUser(appClass, username):

	usrObj = None

	try:
		usrObj = appClass.models.User.objects.get(userId=username)
	except:
		sys.stderr.write("Error: unable to get user from db with id " + username)
		raise

	return usrObj

def getChromosome(appClass, chrNum):
	try:
		chrObj = appClass.models.Chromosome.objects.get(number=int(chrNum))

	except:
		print("Error: unable to get chromosome from db with id " + str(chrNum))
		raise


	return chrObj


def getLocus(appClass, identifier):

	try:
		locusObj = appClass.models.Locus.objects.get(identifier=identifier)

	except:
		print("Error: unable to get locus from db with id " + identifier)
		raise

	return locusObj

def getScheme(appClass, identifier):

	try:
		schObj = appClass.models.Scheme.objects.get(identifier=identifier)

	except:
		sys.stderr.write("Error: unable to get scheme from db with id " + identifier)
		raise

	return schObj

def getSchemes(appClass):
	qs_schemes = None
	try:
		qs_schemes = appClass.models.Scheme.objects.all()
	except:
		sys.stderr.write('Error: unable to get all schemes from db\n')
		raise

	return qs_schemes

def getSchemeGenes(appClass, schemeName):

	try:
		qset_genes = appClass.models.Scheme.objects.get(identifier=schemeName).loci.all()


	except:
		sys.stderr.write("Error: unable to retrieve from db genes of scheme " + schemeName + "\n")
		raise

	return qset_genes

def getAllele(appClass, locus, identifier):

	alleleObj = None
	try:
		alleleObj = appClass.models.Allele.objects.get(locus=locus, identifier=identifier)

	except:
		sys.stderr.write("Error: unable to retrieve from db allele: " + locus + " " +  str(identifier))
		raise
	return alleleObj

def getSnp(appClass, position, original_aa, altered_aa):
	snpObj = None

	try:

		snpObj = appClass.models.Snp.objects.filter(position=int(position), original_aa=original_aa, altered_aa=altered_aa)

	except:
		sys.stderr.write("Error: unable to retrive snp " + str(position) + " " + original_aa + " " + altered_aa)

		raise

	if len(snpObj) > 0:

		return snpObj.get()

	return None

def getAllelicProfile(table0ClassObj, st, dst):

	profObj = None

	try:
		profObj = table0ClassObj.objects.filter(st=st, dst=dst).get()
	except:
		sys.stderr.write("Error: unable to retrieve alleleic profile object " + str(st) + " " + str(dst) + '\n')
		raise

	return profObj


def getCcObj(ccTableObj, ccId, shouldExit):
	ccObj = None
	try:
		ccObj = ccTableObj.objects.filter(identifier=ccId).get()
		return ccObj
	except:
		if shouldExit == False:
			sys.stderr.write("Note: cc object not in db " + str(ccId) + '\n')
		else:
			sys.stderr.write("Note: cc object not in db " + str(ccId) + '\n')
			raise

"""
def getClonalComplex(appClass, schemeName, ccIdentifier, shouldExit):
	ccObj = None

	try:
		ccObj = appClass.models.Clonal_complex.objects.filter(identifier=ccIdentifier, scheme=schemeName).get()

	except:
		if shouldExit == True:
			sys.stderr.write("Error: ")
		else:
			sys.stderr.write("Note: ")

		sys.stderr.write("clonal_complex not in db: " + schemeName + " " + str(ccIdentifier) + '\n')

		if shouldExit == True:
			raise

	return ccObj
"""

def getAllSchemeObjs(appClass):

	qs_schObjs = None

	try:
		qs_schObjs = appClass.models.Scheme.objects.all()

	except:
		sys.stderr.write("Error: unable to get all schemes from the db\n")
		raise

	return qs_schObjs

def getTabNamesSorted(appClass, schemeName):
	tnObjs = None

	try:
		tnObjs = appClass.models.Tables_ap.objects.filter(scheme=schemeName).order_by('table_num')
	except:
		sys.stderr.write("Error: unable to retrieve table names for " + schemeName + '\n')
		raise

	return tnObjs


def getTablesCcObj(appClass, schObj, displayOrder):
	tnObj = None

	try:
		tnObj = appClass.models.Tables_cc.objects.filter(scheme=schObj, display_order=displayOrder).get()

	except:
		sys.stderr.write("Note: cc table name for scheme " + schObj.identifier + " with display order " + displayOrder + " not in Tables_cc " + "\n")
		# raise

	return tnObj


def getTablesApObj(appClass, schObj, tabNum):
	tnObj = None

	try:
		tnObj = appClass.models.Tables_ap.objects.filter(scheme=schObj, table_num=tabNum).get()
		# print (tnObj)

	except:
		sys.stderr.write("Note: ap table name " + str(tabNum) + " for " + schObj.identifier + "  not in Table_name" + "\n")
		# raise

	return tnObj

def get_0_tablesApObj(orgAppClass, schObj):
	tn0Obj = None

	try:
		tn0Obj = orgAppClass.models.Tables_ap.objects.filter(scheme=schObj, table_num = 0).get()

	except():
		sys.stderr.write("Error: cannot get table 0 name for scheme " + schObj.identifier + "\n")
		raise

	return tn0Obj


def getLociSortedInSchemeNoDb(schObj):
	lociObjs = schObj.loci.all().order_by("identifier")
	return lociObjs
