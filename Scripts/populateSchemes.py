import sys
import glob
import re
import addToTableInOrgDb
import readAppSettAndConnToDb
import getFromTableInOrgDb


# COLS OF SCHEMES_INFO_FILE
SCH_NAME = 0
# SCH_ORDER = 1
SCH_UNCERT_TH = 1
SCH_LOCI_FN = 2
SCH_DISP_NAME = 3

################################ MAIN

def addSchemesToDb(projectPath, projectName, appName, fn_schemesInfo, dir_schemeInfo):

	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)

	organismAppClass = readAppSettAndConnToDb.importAppClassModels(appName)


	addTheSchemes(organismAppClass, fn_schemesInfo, dir_schemeInfo)


def addTheSchemes(orgAppClass, fn_schemesInfo, dir_schemeInfo):


	with open(fn_schemesInfo, 'r') as fh_:
		for line in fh_:

			line = line.strip()

			arr = re.split("\t+", line)

			arr[SCH_DISP_NAME] = re.sub("\"", "", arr[SCH_DISP_NAME])

			# schObj = addToTableInOrgDb.addScheme(orgAppClass, arr[SCH_NAME], arr[SCH_UNCERT_TH], arr[SCH_ORDER])
			schObj = addToTableInOrgDb.addScheme(orgAppClass, arr[SCH_NAME], arr[SCH_UNCERT_TH], arr[SCH_DISP_NAME])

			addLociToScheme(orgAppClass, schObj, dir_schemeInfo + arr[SCH_LOCI_FN])

def addLociToScheme(orgAppClass, schObj, fn_lociInScheme):

	with open(fn_lociInScheme, 'r') as fh_:
		for line in fh_:

			line = line.strip()

			locusObj = getFromTableInOrgDb.getLocus(orgAppClass, line)

			addLocusToScheme(schObj, locusObj)
"""
	for filename in glob.glob(dir_schemeInfo + "/*"):
	schemeName = re.sub(".*/", "", filename)
	schemeName = re.sub("\..*$", "", schemeName)


	schObj = addToTableInOrgDb.addScheme(organismAppClass, schemeName)

	with open(filename, 'r') as fh_:

"""

def addLocusToScheme(schObj, locObj):
	try:
		schObj.loci.add(locObj)
		print("Loci " + locObj.identifier +  " added to scheme " + schObj.identifier)
	except:
		sys.stderr.write("Error: unable to add " + locObj.identifier + " to scheme " + schObj.identifier )
		raise


################################ MAIN


def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():
	usage = "python3 script.py <projectPath> <projectName> <appName> <fn_schemesInfo> <SchemeInfoFolderName/>"

	if len(sys.argv) != 6:
		sys.exit("Error: incorrect number of inputs.\n" + usage + '\n\n')

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])
	sys.argv[5] = addSlashIfNotThere(sys.argv[5])

	addSchemesToDb(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])



if __name__ == '__main__':
	main()
