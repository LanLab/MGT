import sys

def updateMergeIdsTo(ccObjsToBeMerged, ccMergeTo):

	for ccObj in ccObjsToBeMerged:
		ccObj.merge_id = ccMergeTo
		ccObj.save()



def addDbFk(appClass, fkId, dbName, url):
	fk = appClass.models.ExternalFks(fkId=fkId, url=url, name=dbName)

	try:
		fk.save()
		sys.stderr.write("Saved metadata fk obj " + str(fkId) + " " + str(dbName) + "\n")
	except:
		sys.stderr.write("Saved matadata fk obj " + str(fkId) + " " + str(dbName) + "\n")
		raise

	return fk


def addIsolation(appClass, source, type, host, hostDisease, date, year):
	i = appClass.models.Isolation(source=source, type=type, host=host, disease=hostDisease, date=date, year=year)

	try:
		i.save()
		sys.stderr.write("Saved isolation "  + str(source) + " " + str(type) + " " + str(host) + " " + str(hostDisease) + " " + str(date) + '\n')
	except:
		sys.stderr.write("Error: unable to save isolation " + str(source) + " " + str(type) + " " + str(host) + " " + str(hostDisease) + " " + str(date) +'\n')
		raise

	return i



def addLocation(appClass, continent, country, state, postcode):
	l = appClass.models.Location(continent=continent, country=country, state=state, postcode=postcode)

	try:
		l.save()
		sys.stderr.write("Saved location " + str(continent) + " " + str(country) + " " + str(state) + " " + str(postcode) + '\n')
	except:
		sys.stderr.write("Error: unable to save location " + str(continent) + " " + str(country) + " " + str(state) + " " + str(postcode) +'\n')
		raise

	return l


def addChromosome(appClass, chrNum, file_loc, refObj):
	c = appClass.models.Chromosome(number=chrNum, file_location=file_loc, reference=refObj)

	try:
		c.save()
		sys.stderr.write("Saved chr " + str(chrNum) + " to db sucessfully\n")
	except:
		sys.stderr.write("Error: unable to save chromosome " + str(chrNum) + "\n")
		raise

def addHst(appClass, dict_hstInfo, dict_table0Names, dict_schObjAps):
	h = appClass.models.Mgt()

	for schObj, (st, dst) in dict_hstInfo.items():
		if not (int(st) == 0 and int(dst) == 0):
			setattr(h, dict_table0Names[schObj].table_name, dict_schObjAps[schObj][(st, dst)])

	try:
		h.save()
		sys.stderr.write("yay, wrote a mgt obj to db\n")
	except:
		sys.stderr.write("error; unable to write a mgt obj to db\n\n")
		raise

	return h




def addIsolate(appClass, projObj, isolateId, server_status, priv_status, file_forward, file_reverse, locObj, isolnObj, fkObj):

	i = appClass.models.Isolate(project=projObj, identifier=isolateId, server_status=server_status, privacy_status=priv_status, file_forward=file_forward, file_reverse=file_reverse, location=locObj, isolation=isolnObj)

	try:
		i.save()

		if fkObj:
			i.extFks.add(fkObj)

		sys.stderr.write("Note: isolate saved succesfully " + isolateId + '\n')
	except:
		sys.stderr.write("Error: unable to save isolate to db " + isolateId + '\n')
		raise

def addProject(appClass, userObj, identifier):

	p = appClass.models.Project(user=userObj, identifier=identifier)

	try:
		p.save()
		sys.stderr.write("Project " + identifier + " saved for user " + userObj.userId + "\n")
		return p
	except:
		sys.stderr.write("Error: unable to save project " +  identifier + " to db  for user " + userObj.userId + '\n')
		raise



def addUser(appClass, username):
	u = appClass.models.User(userId=username)

	try:
		u.save()
		sys.stderr.write("User " + username + " added succesfully to organism database")
	except:
		sys.stderr.write("Error: unable to save to organism database the username " + username + "\n")
		raise



def hromosome(appClass, chromosome, refObj):
	c = appClass.models.Chromosome(number=chromosome["number"], file_location=chromosome["file_location"], reference=refObj)

	try:
		c.save()
		print("Added chromosome succesfully")
	except:
		print("Error: unable to save chromosome to chromosome table")
		raise


def addReference(appClass, jsonObj):
	r = appClass.models.Reference(identifier=jsonObj['identifier'], organism=jsonObj['organism'], description=['description'])

	try:
		r.save()
		print("Added reference succesfully")
	except:
		print("Error: Unable to save to reference table")
		raise

	return r


def addLocus(organismDjangoClass, identifier, loc_start, loc_end, orientation, chrObj, locus_type):

	locus = None
	if not locus_type:
		locus = organismDjangoClass.models.Locus(identifier=identifier, start_location=loc_start, end_location=loc_end, chromosome=chrObj, orientation=orientation)

	else:
		locus = organismDjangoClass.models.Locus(identifier=identifier, start_location=loc_start, end_location=loc_end, locus_type=locus_type, chromosome=chrObj, orientation=orientation)

	try:
		locus.save()
		print("Added locus succesfully " + identifier)
	except:
		print("Error: unable to save to locus table " + identifier)
		raise

	return locus

def addAllele(organismDjangoClass, identifier, locusObj, length, hasSnp, file_location):

	allele = None
	allele = organismDjangoClass.models.Allele(identifier=identifier, locus=locusObj, length=length, hasSnp=hasSnp, file_location=file_location)

	try:
		allele.save()
		print("Added allele succesfully " + str(identifier))
	except:
		print("Error: unable to save to allele table " + str(identifier))
		raise

	return allele

# def addScheme(organismDjangoClass, identifier, uncert_th, orderNum):
def addScheme(organismDjangoClass, identifier, uncert_th, display_name):

	scheme = organismDjangoClass.models.Scheme(identifier=identifier, uncertainty_threshold=uncert_th, display_name=display_name)

	try:
		scheme.save()
		print("Added scheme succesfully " + str(identifier))

	except:
		print("Error: unable to save to scheme table " + str(identifier))
		raise

	return scheme


def addSchemeGroup(orgDjangoClass, identifier):
	schemeGrp = orgDjangoClass.models.Scheme_group(identifier=identifier)

	try:
		schemeGrp.save()
		print("Added scheme group succesfully " + identifier)
	except:
		sys.stderr.write("Error: unable to save to scheme group table " + identifier)
		raise


	return schemeGrp


def addAllelicProfile(appClass, st, dst, schemeObj):

	allelicProfile = appClass.models.Allelic_profile(st=st, dst=dst, scheme=schemeObj)

	try:
		allelicProfile.save()
		print("Added allelic profile: " + schemeObj.identifier + " " + str(st) + " " + str(dst) )

	except:
		sys.stderr.write("Error: unable to save to allelic profile "  + schemeObj.identifier + " " + str(st) + " " + str(dst) )
		raise

	return allelicProfile

def addAlleleToProfile(appClass, allelicProfObj, alleleObj):

	try:
		print("Saved allele to profile: "+ alleleObj.locus.identifier + ":" +  alleleObj.identifier + " " + allelicProfObj.scheme.identifier + ", " + str(allelicProfObj.st) + ", " + str(allelicProfObj.dst))

		allelicProfObj.alleles.add(alleleObj)
		allelicProfObj.save

	except:
		sys.stderr.write("Error: unable to add allele " + alleleObj.identifier + " to allelic profile " + allelicProfObj.st + " " + allelicProfObj.dst)
		raise

def addSnpToAllele(appClass, snpObj, alleleObj):

	try:
		alleleObj.hasSnp = True
		alleleObj.save()

		alleleObj.snps.add(snpObj)

	except:
		sys.stderr.write("Unable to add snp to allele " + alleleObj.locus.identifier + " " + alleleObj.identifier + " " + str(snpObj.position) + " " + snpObj.original_aa + " " + snpObj.altered_aa )
		raise

def addMgtToIsolate(isolateObj, assignmentStatus, mgtObj):

	try:
		isolateObj.server_status = 'C'
		isolateObj.assignment_status = assignmentStatus

		if assignmentStatus == 'A':
			isolateObj.mgt = mgtObj

		isolateObj.save()
		sys.stderr.write("updated isolate to have mgt\n")

	except:
		sys.stderr.write("Error: unable to save mgt to isolate\n")
		raise


def addCcToAllelicProf(ccObj, allelicProfObj, ccTn):

	try:
		setattr(allelicProfObj, ccTn, ccObj)
		allelicProfObj.save()

	except:
		sys.stderr.write("Error: unable to add cc to allelic_profile: " + str(allelicProfObj.st)+ "." + str(allelicProfObj.dst) + " <- " + str(ccObj.identifier))
		raise

def addSnp(appClassObj, position, original_aa, altered_aa):

	snpObj = appClassObj.models.Snp(position=position, original_aa=original_aa, altered_aa=altered_aa)

	try:
		snpObj.save()
		print("Wrote snp object to db " + str(position) + " " + original_aa + " " + altered_aa)
	except:
		sys.stderr.write("Error: unable to save snp " + str(position) + " " + original_aa + " " + altered_aa + '\n')
		raise

	return snpObj

def addClonalComplex(appClassObj, schemeObj, ccIdentifier):

	try:

		ccObj = appClassObj.models.Clonal_complex(scheme=schemeObj, identifier=ccIdentifier)

		# ccObj = appClassObj.models.Clonal_complex(scheme=schemeObj, identifier=ccIdentifier, curr_id=ccObj)

		ccObj.save()

		print("Wrote clonal complex object to db " + str(schemeObj.identifier) + " " + str(ccIdentifier))

	except:
		sys.stderr.write("Error: unable to save clonal complex object to db " + str(schemeObj.identifier) + " " + str(ccIdentifier))
		raise

	return ccObj


def addTablesAp(appClassObj, schObj, tabName, tabNum, displayOrder):

	try:
		tnObj = appClassObj.models.Tables_ap(scheme=schObj, table_num=tabNum, table_name=tabName, display_order=displayOrder)
		tnObj.save()

	except:
		sys.stderr.write("Error: unable to save table name object to db " + schObj.identifier + " " + str(tabNum) + "\n")
		raise



def addTablesCc(orgClass, schObj, tn, tableNum, displayOrder, displayName):
	try:
		tnObj = orgClass.models.Tables_cc(scheme=schObj, table_name=tn, display_table=tableNum, display_order=displayOrder, display_name=displayName)
		tnObj.save()
	except:
		sys.stderr.write("Error: unable to save table name object to db " + schObj.identifier + " " + str(displayOrder) + "\n")
		raise


def addCcToTable(ccTableObj, ccId):
	ccObj = None

	try:
		ccObj = ccTableObj(identifier=ccId)
		ccObj.save()

		sys.stderr.write("Note: save cc obj to db " + str(ccId) + "\n")

		return ccObj

	except:
		sys.stderr.write("Error: unable to save cc obj to db " + str(ccId) + "\n\n")
		raise


def addAllelicProfileStrToTable(tableClassObj, list_names, list_alleleVals, st, dst, tab_0_obj):

	apObj = None

	try:

		if st and dst:
			apObj = tableClassObj(st = st, dst=dst)

		elif tab_0_obj:
			apObj = tableClassObj(main=tab_0_obj)

		else:
			sys.stderr.write("Error missing info, no st, dst, or tab_0 reference provided\n")
			sys.exit()

		setAttributes(apObj, list_names, list_alleleVals)
		apObj.save()

		sys.stderr.write("Note: saved object with st=" + str(st) + " dst=" + str(dst) +'\n')

	except:
		sys.stderr.write("Error: Allelic profile not added to db")
		raise

	return apObj

def setAttributes(apObj, list_names, list_alleleVals):
	for i in range(0, len(list_names)):
		setattr(apObj, list_names[i], list_alleleVals[i])
