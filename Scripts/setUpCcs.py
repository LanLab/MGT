import sys
import getFromTableInOrgDb
import re
import readAppSettAndConnToDb
import math
import addToTableInOrgDb

SCH = 0
TABLE_NUM = 1
DISP_ORD = 2
COL_NAME = 3

################################ TOP_LVL

def genDefs(projectPath, projectName, appName, fn_tablesInfo):

	# dict_tablesInfo = loadTableInfo(fn_tablesInfo)
	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
	organismAppClass = readAppSettAndConnToDb.importAppClassModels(appName)

	genCcCode(organismAppClass, fn_tablesInfo)


################################ AUX

def genCcCode(orgAppClass, fn_tablesInfo):


	with open(fn_tablesInfo, 'r') as fh_:

		for line in fh_:
			line = line.strip()
			arr = line.split("\t")
			tableName = None

			if re.search(r',', arr[TABLE_NUM]):
				arr_tableNum = re.split("[\s]*,[\s]*", arr[TABLE_NUM])
				arr_dispOrd = re.split("[\s]*,[\s]*", arr[DISP_ORD])
				arr_displayName = re.split("[\s]*,[\s]*", arr[COL_NAME])

				for i in range(0, len(arr_tableNum)):
					tableName = checkAndAddToTable(orgAppClass, arr[SCH], arr_tableNum[i], arr_dispOrd[i], arr_displayName[i], tableName)

			else:
				checkAndAddToTable(orgAppClass, arr[SCH], arr[TABLE_NUM], arr[DISP_ORD], arr[COL_NAME], None)

def checkAndAddToTable(orgAppClass, schemeName, tableNum, displayOrd, displayName, tableName):

	tn = getFromTableInOrgDb.getCcTnForScheme(orgAppClass, schemeName, tableNum, displayOrd)


	# print(str(tableName) + " " + str(tn))

	if not tn:
		if not tableName:
			tableName = getTableName(tableNum, displayOrd)
			# and print table code (otherwise no need to print table code).
			printTableCode(tableName)

		schObj = getFromTableInOrgDb.getScheme(orgAppClass, schemeName)

		displayName = re.sub("\"", "", displayName)
		addToTableInOrgDb.addTablesCc(orgAppClass, schObj, tableName, tableNum, displayOrd, displayName)

	else:
		sys.stderr.write("Found tn " + tn.table_name + " " + tn.display_name + ", hence not printing any code\n")


	return tableName


def printTableCode(tableName):

	print ("class " + tableName + "(models.Model):")
	print ("\t" + "identifier = models.IntegerField(primary_key=True)")
	print ("\t" + "merge_id = models.ForeignKey('self', on_delete='PROTECT', blank=True, null=True)")
	print ("\t" + "merge_timestamp = models.DateTimeField(auto_now=True)")
	print ("\t" + "date_created = models.DateTimeField(auto_now_add=True)")
	print ("\t" + "date_modified = models.DateTimeField(auto_now=True)")
	print ("\t" + "def __str__(self):")
	print ("\t\t" + "if self.merge_id:")
	print ("\t\t\t" + "return \"%s: %s, %s\" % (str(self.identifier), str(self.merge_id.identifier), str(self.merge_timestamp))")
	print ("\t\t" + "else:")
	print ("\t\t\t" + "return \"%s: %s, %s\" % (str(self.identifier), \"-\", str(self.merge_timestamp))")
	print ('\n\n');



def getTableName(tableNum, displayOrd):
	return "cc" + tableNum + "_" + displayOrd


################################ MAIN

def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():
	sys.stderr.write("Please note that this script is only recommended to run at setup time (and not for updating the database at a later time) - since mutliple tables may be created for the same information\n\n\n")

	usage = "python3 script.py <projectPath> <projectName> <appName> <tablesInfoFile>"

	if len(sys.argv) != 5:
		sys.exit("Error: incorrect number of inputs\n" + usage + '\n\n')

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])
	genDefs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
