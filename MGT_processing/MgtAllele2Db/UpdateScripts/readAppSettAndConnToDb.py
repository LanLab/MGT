import sys
import os
import django
import json
import importlib
# from Static import *

def setupEnvPath(projectPath, projectName):

	sys.path.append(projectPath)
	os.environ['DJANGO_SETTINGS_MODULE'] = projectName + '.settings'
	django.setup()


def importAppClassModels(appName):
	try:
		appClass = __import__(appName + ".models")
		return appClass

	except:
		sys.exit("Error: application name: " + appName + " not in  specified project settings file.\n")

def importAlleleDirFromSettings(projectName):
	try:
		settingsObj = __import__(projectName + ".settings", globals(), locals(), ['SUBDIR_ALLELES'], 0)
		# print(settingsObj.DIR_ALLELES)
		
		return (settingsObj.MEDIA_ROOT +  settingsObj.SUBDIR_ALLELES)

	except:
		sys.stderr.write("Error: unable to import settings file.\n")
		raise

def importTableName(projectPath, appName, tableName):
	try:
		sys.path.append(projectPath)
		imp = importlib.import_module(appName + ".models.autoGenAps")
		# print ()
		tableClass = getattr(imp, tableName)
		return tableClass
	except:
		sys.stderr.write("Error: unable to import table class.\n")
		raise


def loadJsonFile(jsonFileFullPathName):

	jsonObj = None

	with open(jsonFileFullPathName, 'r') as fh_:
		jsonObj = json.load(fh_)

	if not jsonObj:
		sys.exit("Error: could not read json file, or file empty\n")

	return jsonObj
