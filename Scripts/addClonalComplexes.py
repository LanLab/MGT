import sys
import readAppSettAndConnToDb
import getFromTableInOrgDb
import addToTableInOrgDb
import re


ASSIGN_ST = 0
ASSIGN_DST = 1
ASSIGN_OrigCC = 2
ASSIGN_CurrCC = 3

MERGE_Orig = 0
MERGE_New = 1

################################ TOP_LVL

def doAddClonalComplexes(projectPath, projectName, appName, ccInfoFile, dir_ccFiles):

	# setting up the appClass
	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
	organismAppClass = readAppSettAndConnToDb.importAppClassModels(appName)

	loadAndAddCcs(projectPath, appName, organismAppClass, ccInfoFile, dir_ccFiles)




################################ AUX

def loadAndAddCcs(projectPath, appName, organismAppClass, ccInfoFile, dir_ccFiles):

	# for each line in the file, get the ccTableName, and ccTableObj.
	with open(ccInfoFile, 'r') as fh_:
		for line in fh_:
			line = line.strip()
			(schemeName, fn_assignments, fn_merges, tableNum_orderNum) = line.split("\t")
			(tableNum, tableOdr) = re.split("\_", tableNum_orderNum)

			# getting table names of cc, and ap
			ccTnObj = getFromTableInOrgDb.getCcTn(organismAppClass, tableNum, tableOdr)
			apTnObj = getFromTableInOrgDb.get_0_tablesApObj(organismAppClass, schemeName)

			print (ccTnObj.table_name)

			# get ccTableObj; get apTable0Obj
			ccTableObj = readAppSettAndConnToDb.importTableName(projectPath, appName, ccTnObj.table_name)
			apTable0Obj = readAppSettAndConnToDb.importTableName(projectPath, appName, apTnObj.table_name)

			# print (ccTableObj)
			# print (dir_ccFiles)

			# print (apTable0Obj)

			dict_ccCache = handleAssignments(organismAppClass, apTable0Obj, ccTableObj, ccTnObj.table_name, schemeName, dir_ccFiles + fn_assignments)
			# dict_ccCache = dict()
			handleMerges(dict_ccCache, ccTableObj, dir_ccFiles + fn_merges)

			#for ccObj in ccTableObj.objects.all():
			#	print (str(ccObj.identifier) + "\t" + str(ccObj.merge_id))



################################ CC_MERGES
def handleMerges(dict_ccCache, ccTableObj, pathAndFileCcMerges):

	isHeader = True

	with open(pathAndFileCcMerges, 'r') as fh:
		for line in fh:

			if isHeader == True:
				isHeader = False;
				continue

			line = line.strip()
			arr = line.split('\t')

			ccObj_orig = getOrAddCc(dict_ccCache, ccTableObj, int(arr[MERGE_Orig]))

			ccObj_mergeTo = getOrAddCc(dict_ccCache, ccTableObj, int(arr[MERGE_New]))

			print (str(ccObj_orig.identifier) + "\t" + str(ccObj_mergeTo.identifier))
			if ccObj_mergeTo.merge_id: # 1. get MergeId's mergeId.
				#print ("this one has merge_id")
				#print (" implement 2a ")

				mergedIds_mergedId = ccObj_mergeTo.merge_id;

				ccObjs_toUpdate = getFromTableInOrgDb.getAllCcsWithMergeId(ccTableObj, mergedIds_mergedId.identifier) # 2a. and change to mergeTo
				addToTableInOrgDb.updateMergeIdsTo(ccObjs_toUpdate, ccObj_mergeTo)


				mergedIds_mergedId.merge_id = ccObj_mergeTo
				mergedIds_mergedId.save()

				# ccObj_mergeTo.merge_id.merge_id = ccObj_mergeTo
				# ccObj_mergeTo.merge_id.save()


			ccObjs_toUpdate = getFromTableInOrgDb.getAllCcsWithMergeId(ccTableObj, ccObj_orig.identifier) # 2b. and change to mergeTo.
			addToTableInOrgDb.updateMergeIdsTo(ccObjs_toUpdate, ccObj_mergeTo)

			if ccObj_mergeTo.merge_id:
				if ccObj_mergeTo.identifier == ccObj_mergeTo.identifier: # 3. if it points to itself, then make null
					# print ("points to itself here!" + " " + str(ccObj_mergeTo.identifier))
					ccObj_mergeTo.merge_id = None
					ccObj_mergeTo.save()

			ccObj_orig.merge_id = ccObj_mergeTo # 4.
			ccObj_orig.save()

"""
for ccObj in cc1_3.objects.all():
	try:
		ccObj.merge_id = None
		# ccObj.merge_timestamp = None
		ccObj.save()
	except:
		raise
"""

def mergeNewCcToOrig(ccObj_new, ccObj_orig):
	try:
		ccObj_orig.curr_id = ccObj_new
		ccObj_orig.save()

		sys.stderr.write("Updated orig's curr id " + str(ccObj_orig.identifier) + "\n")

	except:
		sys.stderr.write("Error unable to merge 2 cc's\n");
		raise





################################ AP_TO_CC_ASSIGNMENT

def handleAssignments(orgAppClass, apTable0Obj, ccTableObj, ccTn, schemeName, pathAndFileCcAssign):
	dict_ccCache = dict(); # dict[ccId] = ccObj;

	isHeader = True

	with open(pathAndFileCcAssign, 'r') as fh_:
		for line in fh_:

			line = line.strip()

			if isHeader == True:

				isHeader = False
				continue

			arr = re.split('\t', line)




			if int(arr[ASSIGN_ST]) == 0:
				continue


			# get or add cc Obj
			ccObj = getOrAddCc(dict_ccCache, ccTableObj, int(arr[ASSIGN_OrigCC]))
			# print (ccObj)

			assignCcToAp(apTable0Obj, ccObj, int(arr[ASSIGN_ST]), int(arr[ASSIGN_DST]), ccTn)


	return dict_ccCache



def assignCcToAp(apTable0Obj, ccObj, st, dst, ccTn):

	# print (st, dst)
	try:
		apObj = getFromTableInOrgDb.getAllelicProfile(apTable0Obj, st, dst)

		# if getattr(apObj, ccTn) == ccObj:
		#	sys.stdout.write("Note: Ap " + str(apObj.st) + " " + str(apObj.dst) + " already has cc assigned\n")
		#	return

		addToTableInOrgDb.addCcToAllelicProf(ccObj, apObj, ccTn)
	except:
		print(st,dst,"failed to find st,dst in db")


def getOrAddCc(dict_ccCache, ccTableObj, ccId):
	if ccId in dict_ccCache:
		return dict_ccCache[ccId]

	ccObj = getFromTableInOrgDb.getCcObj(ccTableObj, ccId, False)

	# print ("ccObj here is " + str(ccObj))

	if not ccObj:
		ccObj = addToTableInOrgDb.addCcToTable(ccTableObj, ccId)

	dict_ccCache[ccId] = ccObj

	return ccObj



################################ MAIN

def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():

	usage = "python3 script.py <projectPath> <projectName> <appName> <ccInfoFile.txt> <dir_cc>"

	if len(sys.argv) != 6:
		sys.exit("Error: incorrect number of inputs\n" + usage +'\n\n')

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])
	sys.argv[5] = addSlashIfNotThere(sys.argv[5])

	doAddClonalComplexes(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])


if __name__ == '__main__':
	main()
