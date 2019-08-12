import sys
import os
import json
import re

import readAppSettAndConnToDb
import addToTableInOrgDb
from shutil import copyfile


##################### TOP_LVL


def populateRef(projectPath, projectName, appName, refJsonFile):

	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)

	appClass = readAppSettAndConnToDb.importAppClassModels(appName)

	jsonObj = readAppSettAndConnToDb.loadJsonFile(refJsonFile)

	dir_reference = readAppSettAndConnToDb.importRefDirFromSettings(projectName)

	dir_reference = dir_reference + appName + "/"

	if not os.path.exists(dir_reference):
		os.makedirs(dir_reference)


	refObj = addToTableInOrgDb.addReference(appClass, jsonObj)
	for chromosome in jsonObj["chromosomes"]:
			# print (chromosome)

		chr_fileLoc = cpFileToRightLoc(chromosome['loc_and_filename'], dir_reference)

		addToTableInOrgDb.addChromosome(appClass, chromosome['number'], chr_fileLoc, refObj)




################################ AUXILLARY_CHECK

def cpFileToRightLoc(fn_, dir_to):

	copyfile(fn_, dir_to + os.path.basename(fn_))

	return (dir_to + os.path.basename(fn_))


def checkChrFiles(jsonObj):
	for chromosome in jsonObj["chromosomes"]:
		if not os.path.exists(chromosome["loc_and_filename"]):
			sys.exit("Error: reference chromosome file not found at " + chromosome["file_location"] + '\n' + "Nothing added to database. Exiting.")

	return True
		# print(chromosome["file_location"])

################################ MAIN

def main():
	usage = "python3 script.py <projectPath> <projectName> <appName> <referenceInfoFile.json>\n\n"
	if (len(sys.argv) != 5):
		sys.exit("Error: incorrect number of inputs\n" + usage)


	populateRef(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
