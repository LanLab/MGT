from Salmonella.views.FuncsAuxAndDb import dataExtractTransform as det
from Salmonella.views.FuncsAuxAndDb import queryDb as q

def getAndOfOrQsAndMergedIds(arr_cc, arr_epi):
	dict_mergedIds = dict() # dicts[(ccTn) => list[all_merged_Ids]]

	if len(arr_cc) > 0:
		getMergedIds(dict_mergedIds, arr_cc)

	if len(arr_epi) > 0:
		getMergedIds(dict_mergedIds, arr_epi)

	# print (dict_mergedIds)
	# andOfOrQs = Q()


	andOfOrQs = det.makeAndOfOrQs(dict_mergedIds)

	return (andOfOrQs, dict_mergedIds)


def getMergedIds(dict_mergedIds, arr_cc):
	print (arr_cc)

	for dict_ccTnAndVal in arr_cc:
		for ccTn in dict_ccTnAndVal:

			orQ = det.getOrQ_cc(ccTn, dict_ccTnAndVal[ccTn])

			qs_mergedIds = q.getMergedIds(orQ, ccTn)


			if len(qs_mergedIds) == 0:
				# print("add as empty to dict")
				extractAsList(dict_mergedIds, ccTn, [(dict_ccTnAndVal[ccTn], None)])
			else:
				extractAsList(dict_mergedIds, ccTn, qs_mergedIds)
				# twice the iteration should get complete list (hopefully - since in the first one, the base cc is found...).

				orQ = det.addOrToOrQFromList(orQ, ccTn, dict_mergedIds[ccTn])
				qs_mergedIds = q.getMergedIds(orQ, ccTn)

				extractAsList(dict_mergedIds, ccTn, qs_mergedIds)

	# return dict_mergedIds


def extractAsList(dict_mergedIds, tn, qs_mergedIds):


	if tn not in dict_mergedIds:
		dict_mergedIds[tn] = list()


	for (ccId, ccMergeId) in qs_mergedIds:
		if ccId and ccId not in dict_mergedIds[tn]:
			dict_mergedIds[tn].append(ccId)

		if ccMergeId and ccMergeId not in dict_mergedIds[tn]:
			dict_mergedIds[tn].append(ccMergeId)
