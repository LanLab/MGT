import sys
import re
from MGT_processing.MgtAllele2Db.UpdateScripts import getFromTableInOrgDb, readAppSettAndConnToDb, addToTableInOrgDb

COL_USER = 0
COL_PROJECT = 1
COL_ISOLATE = 2
################################# TOP_LVL

def addTheHstMatrix(projectPath, projectName, appName, mgtlist):

		# setting up the appClass
		readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
		appClass = readAppSettAndConnToDb.importAppClassModels(appName)

		readFileAndAdd(projectPath, appName, appClass, mgtlist)

################################# AUX

def readFileAndAdd(projectPath, appName, appClass, mgtlist):

	# isHeader = True
	#
	# with open(fn_hstMatrix, 'r') as fh_:
	# 	for line in fh_:
	# 		line = line.strip()
	#
	# 		if line:
	# 			## should just need to provide list of[USER, project, isolate_name,MGT2 st.dst,MGT3 st.dst....]
	# 			arr = line.split("\t")

				# if isHeader == True:
	arrhead = "Lanlab	NCBI	Strain 	AssignmentStatus	MGT2	MGT3	MGT4	MGT5	MGT6	MGT7	MGT8	MGT9".split("\t")
	(dict_schObjCols, dict_schObjAps, dict_table0Classes, dict_table0Names,assignStatusCol) = extractSchemeCols(projectPath, appName, appClass, arrhead)

		# isHeader = False
		# continue


	isolateObj = getIsolate(appClass, mgtlist[COL_USER], mgtlist[COL_PROJECT], mgtlist[COL_ISOLATE])

	if isolateObj == None:
		sys.exit("Error: isolate object not found")

	hstObj = None
	if mgtlist[assignStatusCol] == 'A':
		hstObj = createOrGetHstFromDb(appClass, dict_schObjCols, mgtlist, dict_schObjAps, dict_table0Classes,
									  dict_table0Names)

		if hstObj == None:
			sys.stderr.write("Error: Mgt obj not found ... ")
			sys.exit()

	# hstObj = createOrGetHstFromDb(appClass, dict_schObjCols, mgtlist, dict_schObjAps, dict_table0Classes, dict_table0Names)

	# if hstObj == None or isolateObj == None:
	# 	sys.stderr.write("Error: either hgt or isolate obj not found ... ")
	# 	sys.exit()

	addToTableInOrgDb.addMgtToIsolate(isolateObj, mgtlist[assignStatusCol], hstObj)


################################# HST

def createOrGetHstFromDb(appClass, dict_schObjCols, arrLine, dict_schObjAps, dict_table0Classes, dict_table0Names):

	dict_hstInfo = createHstDictAndAddAps(arrLine, dict_schObjCols, dict_schObjAps, dict_table0Classes, dict_table0Names)

	dict_hstQry = genHstQueryDict(dict_hstInfo, dict_table0Names, dict_schObjAps)

	# print (arrLine)
	# print (hstQryStr)

	hstObj = getFromTableInOrgDb.getHst(appClass, dict_hstQry, False)

	# print (hstObj)

	if hstObj == None:
		hstObj = addToTableInOrgDb.addHst(appClass, dict_hstInfo, dict_table0Names, dict_schObjAps)
	else:
		print("MGT object found with id " + str(hstObj.id) + " hence not added to db\n")

	return hstObj


def genHstQueryDict(dict_hstInfo, dict_table0Names, dict_schObjAps):
	dict_hstQry = dict()

	for schObj, (st, dst) in dict_hstInfo.items():


		if int(st) == 0 and int(dst) == 0:
			dict_hstQry[dict_table0Names[schObj].table_name] = None
		else:
			dict_hstQry[dict_table0Names[schObj].table_name] = dict_schObjAps[schObj][(st, dst)].id

	return dict_hstQry



def createHstDictAndAddAps(arrLine, dict_schObjCols, dict_schObjAps, dict_table0Classes, dict_table0Names):

	dict_hstInfo = dict() # dict_[schObj] = (st, dst)


	for schObj, colNum in dict_schObjCols.items():
		if re.search("\.", arrLine[colNum]):
			[st, dst] = re.split("\.", arrLine[colNum], maxsplit=1)
		else:
			st = arrLine[colNum]
			dst = 0

		dict_hstInfo[schObj] = (st, dst)

		if (st, dst) not in dict_schObjAps[schObj]:
			if int(st) == 0 and int(dst) == 0:
				dict_schObjAps[schObj][(st, dst)] = None
			else:
				dict_schObjAps[schObj][(st, dst)] = getFromTableInOrgDb.getAllelicProfile(dict_table0Classes[schObj], int(st), int(dst))

	return dict_hstInfo

################################# ISOLATE


def getIsolate(appClass, username, projectName, isolateName):

	projObj = getFromTableInOrgDb.getProject(appClass, username, projectName, True)
	isolateObj = getFromTableInOrgDb.getIsolate(appClass, projObj, isolateName)

	return isolateObj



################################# HEADER

def extractSchemeCols(projectPath, appName, appClass, arr):

	dict_schObjCols = dict() # dict_[schObj] = colNum
	dict_schObjAps = dict() # dict_[schObj] = list()
	dict_schObjToTable0Class = dict() # dict_[schObj] = table0Class
	dict_table0Names = dict() # dict_[schObj] = table0Name

	assignStatusCol = -1



	schObjs = getFromTableInOrgDb.getSchemes(appClass) # old: get Scheme objects sorted ...

	# print(schObjs)

	for i in range(0, len(arr)):

		if re.match(arr[i], "AssignmentStatus", flags=re.I):
			assignStatusCol = i


		for schObj in schObjs:
			# print(schObj)
			# print(i,arr[i])
			if schObj.identifier.lower() == arr[i].lower():
				dict_schObjCols[schObj] = i
				dict_schObjAps[schObj] = dict()

				tnObj = getFromTableInOrgDb.get_0_tablesApObj(appClass, schObj)
				dict_schObjToTable0Class[schObj] = readAppSettAndConnToDb.importTableName(projectPath, appName, tnObj.table_name)
				dict_table0Names[schObj] = getFromTableInOrgDb.getTablesApObj(appClass, schObj, 0)

				break

	if len(dict_schObjCols) != len(schObjs):
		sys.exit("Error: the input file does not contain all schemes information: " + str(len(dict_schObjCols)) + " " + str(len(schObjs)))

	if assignStatusCol == -1:
		sys.exit("Error: Assignment_status column not provided.")


	return (dict_schObjCols, dict_schObjAps, dict_schObjToTable0Class, dict_table0Names, assignStatusCol)


################################# MAIN

def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():
	usage = "python3 script.py <projectPath> <projectName> <appName> <fn_hstMatrix>"

	if len(sys.argv) != 5:
		sys.exit("Error: incorrect number of inputs\n" + usage + '\n\n')

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])

	addTheHstMatrix(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == '__main__':
	main()
