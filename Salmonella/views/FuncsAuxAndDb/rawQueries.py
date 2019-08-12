from Salmonella.models import View_apcc, Location, Isolation, Isolate, User
from django.db import connections
import sys
import re


def executeQuery_count(queryStr):
	c = connections['salmonella'].cursor()
	c.execute(queryStr)
	iso = c.fetchall()
	c.close()

	return int(iso[0][0])


def executeQuery_table(queryStr):
	c = connections['salmonella'].cursor()

	c.execute(queryStr)
	iso = c.fetchall()

	c.close()

	return (iso)


##################### ISOLATE TABLE JOIN
db_isolate = "\"Salmonella_isolate\" as i"
db_view_apcc = "\"Salmonella_view_apcc\" as v"
db_isolation = "\"Salmonella_isolation\" as iM_i"
db_location = "\"Salmonella_location\" as iM_l"
db_iso_extFks = "\"Salmonella_isolate_extFks\" as i_ext"
db_extFks = "\"Salmonella_externalfks\" as iM_ext"
db_project = "\"Salmonella_project\" as p"

PuStart = 'i.id, i.identifier, i.server_status, i.assignment_status, v.*, iM_l.*, iM_i.*'
PvStart = 'i.id, i.identifier, i.server_status, i.assignment_status, p.identifier, i.privacy_status, v.*, iM_l.*, iM_i.*'
PvStart_projHidden = 'i.id, i.identifier, i.server_status, i.assignment_status, NULL AS project_id, i.privacy_status, v.*, iM_l.*, iM_i.*'
PvStart_projShow = 'i.id, i.identifier, i.server_status, i.assignment_status, p.identifier, i.privacy_status, v.*, iM_l.*, iM_i.*'
Count = 'count(*)'

def getIsolates_auth_proj_cnt(isoSearchStr, projectIds, islnIds, locIds, mgtIds):

	count = 0;

	(queryStr, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, Count, False, False, True)

	queryStr = queryStr + inUserProjSql(projectIds, isAnd) # must be included

	queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, True)


	queryStr = queryStr + ';'

	count = executeQuery_count(queryStr)

	return count


def getIsolates_auth_proj(isoSearchStr, searchedProjIds, islnIds, locIds, mgtIds, offset, limit, orderBy, dir):
	# print('THE ISIOLATES')
	# print(isolates)
	isolates = []

	(queryStr, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, PvStart_projShow, False, False, True)

	queryStr = queryStr + inUserProjSql(searchedProjIds, isAnd)

	queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, True)

	# queryStr (offset and limit)
	queryStr = addTheOrderBy(queryStr, orderBy, dir)
	queryStr = limitTheSearch(queryStr, offset, limit)

	queryStr = queryStr + ';'

	isolates = executeQuery_table(queryStr)

	return isolates




def getIsolates_auth_cnt(isoSearchStr, userProjectIds, islnIds, locIds, mgtIds):

	count = 0;

	(queryStr, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, Count, False, True, True)

	# exclude those in user projects
	if userProjectIds and len(userProjectIds) > 0:
		queryStr = queryStr + notInUserProjSql(userProjectIds)

	queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, isAnd)


	queryStr = queryStr + ';'
	# print (queryStr)

	count = executeQuery_count(queryStr)


	# TODO: COMPLETE THIS SECTION!! [DONE] # get those in uesr projects.
	if len(userProjectIds) > 0:
		count = count + getIsolates_auth_proj_cnt(isoSearchStr, userProjectIds, islnIds, locIds, mgtIds)

	return count

def getIsolates_auth(isoSearchStr, userProjectIds, islnIds, locIds, mgtIds, offset, limit, orderBy, dir):

	isolates = []

	(queryStr, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, PvStart_projHidden, False, True, True)


	# not in user projects
	if userProjectIds and len(userProjectIds) > 0:
		queryStr = queryStr + notInUserProjSql(userProjectIds)


	queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, isAnd)



	# TODO: CHANGE TO UNION (otherwise will end up with more than 100)
	if userProjectIds and len(userProjectIds) > 0:
		queryStr = queryStr + 'UNION ALL('

		(secondSql, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, PvStart_projShow, False, False, True)
		queryStr = queryStr + secondSql
		queryStr = queryStr + inUserProjSql(userProjectIds, isAnd)
		queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, True)

		queryStr = queryStr + ')'

		# print (queryStr)

	queryStr = addTheOrderBy_without(queryStr, orderBy, dir)

	queryStr = limitTheSearch(queryStr, offset, limit)
	queryStr = queryStr + ';'

	# print(queryStr)

	isolates = executeQuery_table(queryStr)
	# print(isolates)


	return isolates


def getIsolates_cnt(isoSearchStr, islnIds, locIds, mgtIds):

	count = 0;

	(queryStr, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, Count, False, True, False)

	queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, isAnd)


	queryStr = queryStr + ';'
	# print (queryStr)

	count = executeQuery_count(queryStr)

	return count



def getIsolates(isoSearchStr, islnIds, locIds, mgtIds, offset, limit, orderBy, dir):

	isolates = []

	(queryStr, isAnd) = sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, PuStart, False, True, False)


	queryStr = addTheSearchParams(queryStr, islnIds, locIds, mgtIds, isAnd)

	queryStr = addTheOrderBy(queryStr, orderBy, dir)

	queryStr = limitTheSearch(queryStr, offset, limit)
	queryStr = queryStr + ';'

	# print (queryStr)
	isolates = executeQuery_table(queryStr)

	return isolates


######################### AUX
def addTheOrderBy(queryStr, orderBy, dir):
	if orderBy and dir:
		queryStr = queryStr + ' ORDER BY ' + orderBy + ' ' + dir + ' ';

	return queryStr

def addTheOrderBy_without(queryStr, orderBy, dir):
	if orderBy and dir:
		orderBy = re.sub("^.*\.", "", orderBy)
		# print(orderBy)

		queryStr = queryStr + ' ORDER BY ' + orderBy + ' ' + dir + ' ';

	return queryStr

def doJoins(sqlStr, mgtIds, locIds, islnIds, isAuth):

	if mgtIds and len(mgtIds) > 0:
		sqlStr = sqlStr + ' INNER JOIN ' + db_view_apcc
	else:
		sqlStr = sqlStr + ' LEFT JOIN ' + db_view_apcc

	sqlStr = sqlStr + ' ON i.mgt_id = v.mgt_id '

	if locIds and len(locIds) > 0:
		sqlStr = sqlStr + ' INNER JOIN ' + db_location
	else:
		sqlStr = sqlStr + ' LEFT JOIN '+ db_location

	sqlStr = sqlStr + ' ON i.location_id = iM_l.id '

	if islnIds and len(islnIds) > 0:
		sqlStr = sqlStr + ' INNER JOIN ' + db_isolation
	else:
		sqlStr = sqlStr + ' LEFT JOIN ' + db_isolation

	sqlStr = sqlStr + ' ON i.isolation_id = iM_i.id '

	if isAuth:
		sqlStr = sqlStr + ' LEFT JOIN ' + db_project
		sqlStr = sqlStr + ' ON i.project_id = p.id '


	return sqlStr


def sqlQueryStruct(isoSearchStr, islnIds, locIds, mgtIds, displayStr, isPriv, isPub, isAuth):
	sqlStr = 'SELECT ' + displayStr + ' FROM ' + db_isolate

	sqlStr = doJoins(sqlStr, mgtIds, locIds, islnIds, isAuth)

	sqlStr = sqlStr + ' WHERE '

	isAnd = False

	if isPriv:
		sqlStr = sqlStr + ' i.privacy_status = \'PV\' '
		isAnd = True

	if isPub:
		sqlStr = sqlStr + ' i.privacy_status = \'PU\' '
		isAnd = True

	if isoSearchStr:
		if not isAnd:
			isoSearchStr = re.sub("^[\s]+AND", "", isoSearchStr, flags=re.I)
			isAnd = True

		sqlStr = sqlStr + isoSearchStr

	return (sqlStr, isAnd)


def limitTheSearch(queryStr, offset, limit):
	queryStr = queryStr + ' OFFSET ' + str(offset) + ' LIMIT ' + str(limit)
	return (queryStr)


def notInUserProjSql(userProjIds):
	return (' AND i.project_id != ALL(ARRAY' + str(userProjIds) + ') ')

def inUserProjSql(projIds, isAnd):
	theStr = ""

	if isAnd:
		theStr = ' AND '

	isAnd = True

	return (theStr + ' i.project_id = ANY(ARRAY' + str(projIds) + ') ')

def addTheSearchParams(queryStr, islnIds, locIds, mgtIds, isAnd):
	if mgtIds and len(mgtIds) > 0:
		if isAnd:
			queryStr = queryStr + ' AND '

		queryStr = queryStr + ' v.mgt_id = ANY(ARRAY' +  str(list(mgtIds)) +') '
		isAnd = True

	if islnIds and len(islnIds) > 0:
		if isAnd:
			queryStr = queryStr + ' AND '

		queryStr = queryStr + ' iM_i.id = ANY(ARRAY' +  str(list(islnIds)) +') '
		isAnd = True

	if locIds and len(locIds) > 0:
		if isAnd:
			queryStr = queryStr + ' AND '

		queryStr = queryStr + ' iM_l.id = ANY(ARRAY' +  str(list(locIds)) +') '
		isAnd = True

	return queryStr
