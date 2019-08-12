import math

def ownPaginator(totalIsolates, page, totalIsolatesPerPage):

		pageAttrs = ["has_other_pages", "has_next", "has_previous", "next_page_number", "previous_page_number", "start_index", "end_index", "num_pages", "total_count", "page"]
		dict_pageInfo = dict.fromkeys(pageAttrs, None)

		dict_pageInfo['total_count'] = totalIsolates
		dict_pageInfo['page'] = page
		dict_pageInfo['num_pages'] = math.ceil(dict_pageInfo['total_count'] / totalIsolatesPerPage)

		if dict_pageInfo['num_pages'] > 1:
			dict_pageInfo['has_other_pages'] = True

			if page == 1:
				dict_pageInfo['has_previous'] = False
				dict_pageInfo['has_next'] = True

			elif page == dict_pageInfo['num_pages']:
				dict_pageInfo['has_next'] = False
				dict_pageInfo['has_previous'] = True

			else:
				dict_pageInfo['has_next'] = True
				dict_pageInfo['has_previous'] = True


			if dict_pageInfo['has_next'] == True:
				dict_pageInfo['next_page_number'] = page + 1

			if dict_pageInfo['has_previous'] == True:
				dict_pageInfo['previous_page_number'] = page - 1

		else:
			dict_pageInfo['has_other_pages'] = False


		dict_pageInfo['start_index'] = (page - 1) * totalIsolatesPerPage
		if dict_pageInfo['page'] == dict_pageInfo['num_pages']: # last page
			dict_pageInfo['end_index'] = dict_pageInfo['total_count'] % totalIsolatesPerPage
		else: # not the last page
			dict_pageInfo['end_index'] = dict_pageInfo['start_index'] + (totalIsolatesPerPage - 1)

		return dict_pageInfo
