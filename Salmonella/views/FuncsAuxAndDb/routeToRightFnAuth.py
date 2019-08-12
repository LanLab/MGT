from . import queryDb as q
from . import ownPaginator as ownPaginator
import re
from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from django.db.models import Q
from Salmonella.views.FuncsAuxAndDb import rawQueries
from Salmonella.views.FuncsAuxAndDb import getPoolOfCcMergeIds as getCcMergeIdsList
from Salmonella.models import Project, User


def getMgtIds(arr_ap, arr_cc, arr_epi):

	qs_mgtIds = None

	# for cc_query, and cc_mergeIds
	andOfOrQs = Q()
	dict_mergedIds = dict()

	if len(arr_cc) > 0 or len(arr_epi) > 0: # cc and epi query (combine into 1)
		(andOfOrQs, dict_mergedIds) = getCcMergeIdsList.getAndOfOrQsAndMergedIds(arr_cc, arr_epi)


	if len(arr_ap) > 0: # ap query
		andOfOrQs = det.addToAndQFromList(andOfOrQs, arr_ap)

	# getting the mgt ids.
	qs_mgtIds = q.getMgtIdsFromViewWithQ(andOfOrQs)
	# print("qs_mgtIds: ")
	# print(qs_mgtIds)
	return (qs_mgtIds, dict_mergedIds)


def getLocIds(arr_loc):
	qs_location = None

	andQ_loc = Q()
	andQ_loc = det.addToAndQICntnsFromList(andQ_loc, arr_loc)
	qs_location = q.getLocationIdsWithQ(andQ_loc)

	return qs_location

def getIslnIds(arr_isln):
	qs_isln = None

	andQ_isln = Q()

	for dict_ in arr_isln:
		for key in dict_:
			if re.match("year", key) or re.match("date", key):
				# print (key);
				andQ_isln = det.addToAndQFromList(andQ_isln, [dict_])

			else:
				andQ_isln = det.addToAndQICntnsFromList(andQ_isln, [dict_])

	qs_isln = q.getIsolnIdsWithQ(andQ_isln)
	return (qs_isln)




def makeSearchStr_retProjIdsIfSearProj(arr_iso, username, isExactProj):

	searchStr = "";
	projectIds = []

	for dict_ in arr_iso:
		for key in dict_:
			if re.match("server_status", key) or re.match("privacy_status", key) or re.match("assignment_status", key):
				searchStr = searchStr + " and i." + key +"=\'" + dict_[key] + "\'";

			elif username and re.match("project", key) and isExactProj == False:

				projectIds = q.getAndAddProjectIds(username, dict_[key], projectIds)

				# print("project ids are :::")
				# print(projectIds)
				# searchStr = searchStr + " and i.project=\'" + dict_[key] + "\'";
				if len(projectIds) == 0:
					print("Project belongs to someone else")
					raise IncorrectAccessError("Project belongs to someone else")

			elif username and re.match("project", key) and isExactProj == True:
				if not isProjectByUser(dict_[key], username):
					print("Project belongs to someone else")
					raise IncorrectAccessError("Project belongs to someone else")
				projectIds = [int(dict_[key])]
				# print("project ids are :::")
				# print(projectIds)
			elif re.match("identifier", key):
				searchStr = searchStr + " and i.identifier ILIKE \'%" + dict_[key] + "%\'"

			else:
				print("Unknown key supplied")
				raise IncorrectAccessError("Unknown key supplied")

	# print (searchStr);
	return (searchStr, projectIds)

class IncorrectAccessError(Exception):
	"""Raise when user searched for strings which did not return any ids in the database"""

def isProjectByUser(projectId, username):
	if Project.objects.filter(id=int(projectId),user=User.objects.get(userId=username)).exists():
		return True

	return False


def convertSearchToIds(arr_ap, arr_cc, arr_epi, arr_loc, arr_isln, arr_iso, username, isExactProj):
	mgtIds = None # querySets
	locIds = None
	islnIds = None
	isoSearchStr = ""
	searchedProjIds = [] # searched project ids
	userProjIds = [] #
	dict_mergedIds = dict()

	if len(arr_ap) > 0 or len(arr_cc) > 0 or len(arr_epi) > 0:
		(mgtIds, dict_mergedIds) = getMgtIds(arr_ap, arr_cc, arr_epi)

		if not mgtIds or len(mgtIds) == 0:
			raise IncorrectAccessError('Mgt ids not found.') # nothing found, so return empty

		# if len(dict_mergedIds) > 0:
		# 	print(dict_mergedIds)
		#	print("need to do something here...")

	if len(arr_loc) > 0:
		locIds = getLocIds(arr_loc)

		if not locIds or len(locIds) == 0: # nothing found
			raise IncorrectAccessError('Loc ids not found.')

	if len(arr_isln) > 0:
		islnIds = getIslnIds(arr_isln)

		if not islnIds or len(islnIds) == 0:
			raise IncorrectAccessError('Isln ids not found.')

	if len(arr_iso) > 0:
		(isoSearchStr, searchedProjIds) = makeSearchStr_retProjIdsIfSearProj(arr_iso, username, isExactProj)
		# print ("The searched project ids are: " + str(searchedProjIds))

		if isoSearchStr == "" and len(searchedProjIds) == 0: # empty search string
			print("No iso to features to search")
			raise IncorrectAccessError('No iso to features to search')

	if username:
		userProjIds = q.getUserProjectIds(username)
		# print (userProjIds)
		if (len(searchedProjIds) > 0 and len(userProjIds) == 0) or not set(searchedProjIds).issubset(set(userProjIds)):
			# print("Searched projects when either user hasnt created any projects or the searched project is not a user project")
			raise IncorrectAccessError('Searched projects when either user hasnt created any projects or the searched project is not a user project')

	return (mgtIds, locIds, islnIds, isoSearchStr, searchedProjIds, userProjIds, dict_mergedIds)

def convertToQueriableFields(orderBy, dir):
	if dir == 'Ascending':
		dir = 'ASC'
	elif dir == 'Descending':
		dir = 'DESC'

	return (orderBy, dir);


### MAIN: AUTH (and non-auth) based search
def getIsolatesFromRightFn(arr_ap, arr_cc, arr_epi, arr_loc, arr_isln, arr_iso, pageNumToGet, totalPerPage, username, isExactProj, orderBy, dir):

	# print(" BUT DO WE STILL COME INTO THIS FUNCTION? ")

	isoCount = 0
	isolates = [];
	dict_pageInfo = ownPaginator.ownPaginator(0, 0, totalPerPage)
	dict_mergedIds = dict()

	(orderBy, dir) = convertToQueriableFields(orderBy, dir)

	try:
		(mgtIds, locIds, islnIds, isoSearchStr, searchedProjIds, userProjIds, dict_mergedIds) = convertSearchToIds(arr_ap, arr_cc, arr_epi, arr_loc, arr_isln, arr_iso, username, isExactProj)
	except IncorrectAccessError:
		print("Incorrect access error encoutered.")
		return (isoCount, isolates, dict_pageInfo, dict_mergedIds)

	# if len(projectIds) == 0:
		# print(userProjectIds)

	# print(searchedProjIds)
	# print(isoSearchStr)
	print("this time over here!")

	if len(searchedProjIds) > 0: # if projects are searched for
		isoCount = rawQueries.getIsolates_auth_proj_cnt(isoSearchStr, searchedProjIds, islnIds, locIds, mgtIds)

		dict_pageInfo = ownPaginator.ownPaginator(isoCount, pageNumToGet, totalPerPage)

		isolates = rawQueries.getIsolates_auth_proj(isoSearchStr, searchedProjIds, islnIds, locIds, mgtIds, dict_pageInfo['start_index'], dict_pageInfo['end_index'], orderBy, dir)


		# print("THE ISOLATES")
		# print (isolates)

	elif username: # if projects are not searched for; but user is logged in
		isoCount = rawQueries.getIsolates_auth_cnt(isoSearchStr, userProjIds, islnIds, locIds, mgtIds)

		dict_pageInfo = ownPaginator.ownPaginator(isoCount, pageNumToGet, totalPerPage)

		isolates = rawQueries.getIsolates_auth(isoSearchStr, userProjIds, islnIds, locIds, mgtIds, dict_pageInfo['start_index'], dict_pageInfo['end_index'], orderBy, dir)
		print("least thought of!")
	else: # user is not logged in

		isoCount = rawQueries.getIsolates_cnt(isoSearchStr, islnIds, locIds, mgtIds)

		dict_pageInfo = ownPaginator.ownPaginator(isoCount, pageNumToGet, totalPerPage)

		isolates = rawQueries.getIsolates(isoSearchStr, islnIds, locIds, mgtIds, dict_pageInfo['start_index'], dict_pageInfo['end_index'], orderBy, dir)

	return (isoCount, isolates, dict_pageInfo, dict_mergedIds)
