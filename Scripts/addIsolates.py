# 1. username must exist in db_username (else quit) # might be usefule in the future "https://stackoverflow.com/questions/8047204/django-script-to-access-model-objects-without-using-manage-py-shell?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa"

# 2. if username does not exist in db_appname, add to table
# 3. if projectName not in db, add to project table
# 4. add/update isolate in db

import sys
import re
import readAppSettAndConnToDb
import addToTableInOrgDb
import getFromTableInOrgDb
from datetime import datetime
from django.utils.dateparse import parse_date

Col_username = 0
Col_projectName = 1
Col_privStatus = 2
Col_isolateId = 3

## Meta data fields

# location
# Col_continent = 13 # file isolate_metadata_.txt
# Col_country = 12 # file isolate_metadata_.txt
Col_continent = 11 # file isolate_info.txt
Col_country = 10 # file isolate_info.txt
Col_state = 9 # file isolate_info.txt
Col_postcode = 8 # file isolate_info.txt

# isolation
# Col_source = 15 # file isolate_metadata_.txt
# Col_type = 16 # file isolate_metadata_.txt
# Col_host = 17 # file isolate_metadata_.txt
# Col_hostDisease = 18 # file isolate_metadata_.txt
# Col_date = 10 # file isolate_metadata_.txt

Col_source = 13 # file isolate_metadata_.txt
Col_type = 14 # file isolate_metadata_.txt
Col_host = 15 # file isolate_metadata_.txt
Col_hostDisease = 16 # file isolate_metadata_.txt
Col_date = 6 # file isolate_metadata_.txt
Col_year = 7

# external fks
## NCBI
# Col_fkId = 5 # file isolate_metadata_.txt
# Col_dbName = 4 # file isolate_metadata_.txt
# Col_url =


# TODO: swap col_privStatus and col_isolateId in input file
# TODO: always check file_forward and file_reverse exist and are in the right position before adding.

################################# TOP_LVL

def addInfo(projectPath, projectName, appName, fn_isolateInfo):

	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)


	appClass = readAppSettAndConnToDb.importAppClassModels(appName)

	from django.contrib.auth.models import User
	handleTheFile(User, appClass, fn_isolateInfo)

################################# AUX


def handleTheFile(User, appClass, fn_isolateInfo):
		dict_username = dict() # dict[username] = userObj
		dict_projectName = dict() # dict[(username, projectName)] => projObj

		dict_md_location = dict()
		dict_md_isolation = dict()
		dict_md_extFks = dict()

		with open(fn_isolateInfo, 'r') as fh_:

			isHeader = True

			for line in fh_:

				if isHeader == True:
					isHeader = False
					continue


				line = re.sub('[\n\r]+$', '', line)
				arr = line.split("\t")

				handleUsername(User, appClass, dict_username, arr[Col_username])

				handleProject(appClass, dict_projectName, arr[Col_username], arr[Col_projectName], dict_username[arr[Col_username]])


				locObj = handleLocation(appClass, dict_md_location, arr[Col_continent], arr[Col_country], arr[Col_state], arr[Col_postcode])
				# locObj = handleLocation(appClass, dict_md_location, arr[Col_continent], arr[Col_country], "", "")  # file isolate_metadata_.txt

				isolnObj = handleIsolation(appClass, dict_md_isolation, arr[Col_source], arr[Col_type], arr[Col_host], arr[Col_hostDisease], arr[Col_date], arr[Col_year])

				# fkObj = handleFks(appClass, dict_md_extFks, arr[Col_fkId], arr[Col_dbName], "") # file isolate_metadata_.txt
				fkObj = None

				handleIsolate(appClass, dict_projectName[(arr[Col_username], arr[Col_projectName])], arr[Col_isolateId], arr[Col_privStatus], locObj, isolnObj, fkObj)




################################# METADATA
def makeNoneIfEmpty(val):
	if val == "" or re.match('^Unknown$', val, flags=re.I):
		return None

	return val

##################### Fks

def handleFks(appClass, dict_md_extFks, fkId, dbName, url):

	fkId = makeNoneIfEmpty(fkId)
	dbName = makeNoneIfEmpty(dbName)
	url = makeNoneIfEmpty(url)

	if (fkId == None):
		return None

	if (fkId, dbName) not in dict_md_extFks:
		fkObj = getFromTableInOrgDb.getDbFk(appClass, fkId, dbName)

		if fkObj == None:
			fkObj = addToTableInOrgDb.addDbFk(appClass, fkId, dbName, url)

		dict_md_extFks[(fkId, dbName)] = fkObj

	return dict_md_extFks[(fkId, dbName)]



##################### Isolation

def handleIsolation(appClass, dict_md_isolation, source, type, host, hostDisease, date, year):
	# print (date)

	source = makeNoneIfEmpty(source)
	type = makeNoneIfEmpty(type)
	host = makeNoneIfEmpty(host)
	hostDisease = makeNoneIfEmpty(hostDisease)
	date = makeNoneIfEmpty(date)
	year = makeNoneIfEmpty(year)

	date_formated = None


	if (source == None and type == None and host == None and hostDisease == None and date == None and year == None):
		# print ("here!")
		return None

	if date != None and re.search("\/", date):
		arr = re.split("\/", date)

		# print(arr[0] + "\t" + arr[1] + "\t" + arr[2] + "\t" + year)
		date_formated = datetime(int(year), int(arr[1]), int(arr[0]))

		# print(date_formated.date())


	if (source, type, host, hostDisease, date_formated, year) not in dict_md_isolation:
		iObj = getFromTableInOrgDb.getIsolation(appClass, source, type, host, hostDisease, date_formated, year)

		if iObj == None:
			iObj = addToTableInOrgDb.addIsolation(appClass, source, type, host, hostDisease, date_formated, year)

		dict_md_isolation[(source, type, host, hostDisease, date_formated, year)] = iObj

	return dict_md_isolation[(source, type, host, hostDisease, date_formated, year)]


##################### Location

def handleLocation(appClass, dict_md_location, continent, country, state, postcode):

	# print (continent + " " + country + " " + state + " " + postcode)
	continent = makeNoneIfEmpty(continent)
	country = makeNoneIfEmpty(country)
	state = makeNoneIfEmpty(state)
	postcode = makeNoneIfEmpty(postcode)

	if continent == None and country == None and state == None and postcode == None:
		return None

	if (continent, country, state, postcode) not in dict_md_location:
		locObj = getFromTableInOrgDb.getLocation(appClass, continent, country, state, postcode)

		if locObj == None:

			locObj = addToTableInOrgDb.addLocation(appClass, continent, country, state, postcode)


		dict_md_location[(continent, country, state, postcode)] = locObj
			# add to Db, add returned obj to dict_


	return dict_md_location[(continent, country, state, postcode)]




	# if not appClass.models.Location.objects.filter(continent=continent, country=country, state=state, postcode=postcode):

		# print ("here!")
		#locObj = addToTableInOrgDb.addLocation()

		#dict_md_location[(continent, country, state, postcode)] = locObj



################################# PT_4-isolate
def handleIsolate(appClass, projObj, isolateName, privStatus, locObj, isolnObj, fkObj):

	if not appClass.models.Isolate.objects.filter(identifier=isolateName, project=projObj):

		privStatusCode = getPrivStatusCode(privStatus)

		addToTableInOrgDb.addIsolate(appClass, projObj, isolateName, 'U',  privStatusCode, None, None, locObj, isolnObj, fkObj)

	else:

		sys.stderr.write("Note: isolate with id " + isolateName + " already exists in project " + projObj.identifier +  " for user " + projObj.user.userId + "\n")


def getPrivStatusCode(privStatusStr):
	if re.match("public", privStatusStr, flags=re.I):
		return "PU"

	elif re.match("private", privStatusStr, flags=re.I):
		return "PV"

	else:
		sys.exit("error: unknown privacy status code " + privStatusStr + ". Allowed are public and private.\n")


################################# PT_3-project

def handleProject(appClass, dict_projectName, username, projectName, userObj):

	if (username, projectName) not in dict_projectName:

		projObj = getFromTableInOrgDb.getProject(appClass, username, projectName, False)

		if projObj == None:

			projObj = addToTableInOrgDb.addProject(appClass, userObj, projectName)


		dict_projectName[(username, projectName)] = projObj


#################################-PT_1_&_2_ user
def handleUsername(User, appClass, dict_username, username):

	if username not in dict_username:

		if not isUserNameInUserDb(User, username): # check in user db
			sys.exit("Error: username " + username + " much exist in database. Please create this user then come back\n");

		addUserIfNotInAppDb(appClass, username)


		userObj = getFromTableInOrgDb.getUser(appClass, username)
		dict_username[username] = userObj






def addUserIfNotInAppDb(appClass, username):

	if not appClass.models.User.objects.filter(userId=username).exists():
		addToTableInOrgDb.addUser(appClass, username)




def isUserNameInUserDb(User, username):

	if User.objects.filter(username=username).exists():
		return True

	return False


################################# MAIN

def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():

	usage = "python3 script.py <projectPath> <projectName> <appName> <fn_isolateInfo>"

	if len(sys.argv) != 5:
		sys.stderr.write("Error: incorrect number of input arguments\n" + usage + '\n\n')
		sys.exit()

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])

	addInfo(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
