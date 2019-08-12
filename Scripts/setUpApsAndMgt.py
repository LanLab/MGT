import sys
import getFromTableInOrgDb
import re
import readAppSettAndConnToDb
import math
import addToTableInOrgDb

PGS_COL_LIMIT = 1000 # although pgs col limit is 1600, there is a buffer to allow for additional columns such as date created, modified, clonal_complex.

################################ TOP_LVL

def genDefs(projectPath, projectName, appName, fn_tablesInfo):

	dict_tablesInfo = loadTableInfo(fn_tablesInfo)
	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
	organismAppClass = readAppSettAndConnToDb.importAppClassModels(appName)

	genApCode(organismAppClass, dict_tablesInfo)


################################ AUX


def loadTableInfo(fn_tablesInfo):
	dict_tablesInfo = dict() # dict[schemeName] = display_order
	with open(fn_tablesInfo, 'r') as fh_tablesInfo:
		for line in fh_tablesInfo:
			line = line.strip()
			(schemeName, displayOrder) = line.split("\t")

			dict_tablesInfo[schemeName] = displayOrder

	return dict_tablesInfo


def genApCode(organismAppClass, dict_tablesInfo):

	# 1. obtain all schemeObjs from the db
	qs_schObjs = getFromTableInOrgDb.getAllSchemeObjs(organismAppClass)

	# 2. for each schemeObj, create def skeleton in list, then add locus
	for schObj in qs_schObjs:
		# print(schObj.loci.all())
		totalTabNums = getTableNumsForSch(schObj)
	#	print (totalTabNums)
	# 	print (schObj.loci.count())
		ap_tableName_0 = None

		for tabNum in range(0, totalTabNums):
			ap_tableName = getTableName(tabNum, dict_tablesInfo[schObj.identifier])

			if tabNum == 0:
				ap_tableName_0 = ap_tableName

			addTableNameInDb(organismAppClass, ap_tableName, schObj, tabNum, dict_tablesInfo[schObj.identifier])


			list_code = createTableCode(organismAppClass, schObj, tabNum, ap_tableName, ap_tableName_0)
			printTableCode(list_code)

	list_code = createHstCode(organismAppClass, qs_schObjs)
	printTableCode(list_code)


####################### OUTPUT

def printTableCode(list_code):
	for outLine in list_code:
		print (outLine)
	print ()
	print ()

####################### SETTING UP THE TABLE
def getTableNumsForSch(schObj):

	if schObj.loci.count() >= PGS_COL_LIMIT:
		# print ("Split here " + schObj.identifier)
		return math.ceil(schObj.loci.count()/PGS_COL_LIMIT)

	return 1


def createHstCode(orgAppClass, qs_schObjs):
	list_code = list()

	list_code.append("class Mgt(models.Model):")

	uniqueTogetherStr = "\t\tunique_together = (("
	for schObj in qs_schObjs:
		tn0Obj = getFromTableInOrgDb.get_0_tablesApObj(orgAppClass, schObj)
		# print (tn0Obj.table_name)
		list_code.append("\t" + tn0Obj.table_name + " = models.ForeignKey(" + tn0Obj.table_name + ", on_delete=models.PROTECT, blank=True, null=True)")

		# list_code.append("\t" + tn0Obj.table_name + "cc " + " = models.ForeignKey(" + tn0Obj.table_name + ", on_delete=models.PROTECT, blank=True, null=True)")

		uniqueTogetherStr = uniqueTogetherStr + "\"" + tn0Obj.table_name + "\", "
		# list_code.append("\t" + "st" + schObj.table_name + " = models.ForeignKey(" +  schObj.table_name + ",  on_delete=models.PROTECT)")
		# list_code.append("\t" + "dst" +  schObj.table_name +   " = models.ForeignKey(" + schObj. + ", on_delete=models.PROTECT)")


	uniqueTogetherStr = uniqueTogetherStr + "))"

	list_code.append("\tclass Meta:")
	list_code.append(uniqueTogetherStr)

	return list_code



def addTableNameInDb(orgAppClass, tableName, schObj, tabNum, displayOrder):

	tnObj = getFromTableInOrgDb.getTablesApObj(orgAppClass, schObj, tabNum)

	# print (tnObj)
	if tnObj:
		sys.stderr.write("Found table object " + tnObj.scheme.identifier + " " + displayOrder + "\n")
	if not tnObj:
		addToTableInOrgDb.addTablesAp(orgAppClass, schObj, tableName, tabNum, displayOrder)



	# try:
	#	schObj.table_name = ap_tableName
	#	schObj.save()
	#except:
	#	sys.stderr.write("Error: unable to update scheme table\n")
	#	raise


def getTableName(tabNum, displayOrder):
	# tableName = re.sub("_", "", tableName)
	#if re.match("^[0-9]", tableName):
	# tableName = "t" + str(tabNum) + "_" + tableName

	tableName = "ap" + str(displayOrder) + "_" + str(tabNum)
	return tableName




def createTableCode(appClass, schObj, tabNum, tableName, table_0_name):

	list_code = list()
	(startCount, endCount) = getStartAndEnd(int(tabNum))

	list_code.append("class " + tableName + "(models.Model):")

	if tableName == table_0_name :
		list_code.append("\t" + "st = models.IntegerField()")
		list_code.append("\t" + "dst = models.IntegerField()")
		# list_code.append("\t" + "clonal_complex = models.ForeignKey(Clonal_complex, on_delete='PROTECT', blank=True, null=True)")

		# list_code.append("\t" + "scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT)")
		appendClonalComplexFks(appClass, schObj, list_code)

		list_code.append("\t" + "class Meta:")
		list_code.append("\t" + "\t" + "unique_together = ((\"st\", \"dst\"),)")

		list_code.append("\t" + "def __str__(self):")
		list_code.append("\t" + "\t" + "return \"%s.%s\" % (str(self.st), str(self.dst))")

	else:
		list_code.append("\t" + "main = models.OneToOneField(" + table_0_name + ", on_delete=models.PROTECT, primary_key=True, related_name='+',)")

		list_code.append("\t" + "def __str__(self):")
		list_code.append("\t" + "\t" + "return \"%s, %s.%s\" % (str(self.main.st), str(self.main.dst))")


	appendGeneCols(list_code, schObj, startCount, endCount)


	# date created & date modified
	list_code.append("\t" + "date_created = models.DateTimeField(auto_now_add=True)")
	list_code.append("\t" + "date_modified = models.DateTimeField(auto_now=True)")

	return list_code


def getStartAndEnd(tabNum):
	s = 1000 * tabNum
	e = 1000 * (tabNum + 1)

	return (s, e)


def appendGeneCols(list_code, schObj, startCount, endCount):

	count = startCount

	# print (schObj)
	loci = getFromTableInOrgDb.getLociSortedInSchemeNoDb(schObj)

	for i in range(startCount, endCount):
		if i > len(loci)-1:
			break

		locIdent = re.sub("\_", "", loci[i].identifier)
		list_code.append("\t" + locIdent + " = models.CharField(max_length=50)")


def appendClonalComplexFks(appClass, schObj, list_code):

	qs_tns = getFromTableInOrgDb.getCcTnsForScheme(appClass, schObj)

	for tnObj in qs_tns:
		list_code.append("\t" + tnObj.table_name + " = models.ForeignKey(" + tnObj.table_name + ", on_delete='PROTECT', blank=True, null=True)")




################################ MAIN

def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():

	usage = "python3 script.py <projectPath> <projectName> <appName> <tablesInfoFile>"

	if len(sys.argv) != 5:
		sys.exit("Error: incorrect number of inputs\n" + usage + '\n\n')

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])
	genDefs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
