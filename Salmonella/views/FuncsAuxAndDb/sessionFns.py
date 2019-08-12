import json

def loadIfInSession(sessionVar, key, default):
	if key in sessionVar[0]:
		return (sessionVar[0][key])

	return default


def loadSessionSearchVars(sessionVar):
	arr_ap = sessionVar[0]['arrAp']
	arr_cc = sessionVar[0]['arrCc']
	arr_epi = sessionVar[0]['arrEpi']
	arr_iso = sessionVar[0]['arrIso']
	arr_isln = sessionVar[0]['arrIsln']
	arr_loc = sessionVar[0]['arrLoc']

	return (arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc)

def loadSessionSearchVars_detail(sessionVar):
	searchAp = sessionVar[0]['json_apSearchTerms']
	searchCcEpi = sessionVar[0]['json_ccEpiSearchTerms']
	searchLocs = sessionVar[0]['json_location']
	searchIsln = sessionVar[0]['json_isolation']
	searchProj = sessionVar[0]['json_project']

	return (searchAp, searchCcEpi, searchLocs, searchIsln, searchProj)

def isASearchPresent_detail(requestVar):
	if ('json_apSearchTerms' in requestVar and len(requestVar['json_apSearchTerms']) > 0) or  ('json_ccEpiSearchTerms' in requestVar and len(requestVar['json_ccEpiSearchTerms']) > 0) or  ('json_location' in requestVar and len(requestVar['json_location']) > 0) or ('json_isolation' in requestVar and len(requestVar['json_isolation']) > 0) or ('json_project' in requestVar and len(requestVar['json_project']) > 0):
	 	return True

	return False


def isASearchPresent(sessionVar):
	if ('arrAp' in sessionVar and len(sessionVar['arrAp']) > 0) or ('arrCc' in sessionVar and len(sessionVar['arrCc']) > 0) or ('arrEpi' in sessionVar and len(sessionVar['arrEpi']) > 0) or ('arrIso' in sessionVar and len(sessionVar['arrIso']) > 0) or ('arrIsln' in sessionVar and len(sessionVar['arrIsln']) > 0) or ('arrLoc' in sessionVar and len(sessionVar['arrLoc']) > 0):
		return True

	return False


def loadRequestSearchVars(requestVar):
	arr_ap = json.loads(requestVar['arrAp'])
	arr_cc = json.loads(requestVar['arrCc'])
	arr_epi = json.loads(requestVar['arrEpi'])
	arr_iso = json.loads(requestVar['arrIso'])
	arr_isln = json.loads(requestVar['arrIsln'])
	arr_loc = json.loads(requestVar['arrLoc'])

	return (arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc)
