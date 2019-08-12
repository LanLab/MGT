from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from Mgt.settings import APPS_DATABASE_MAPPING
import sys

def page(request):
# return HttpResponse('a users project management page')
#return render()
	app_db_mapping = APPS_DATABASE_MAPPING

	userStats = getUserStatistics(request.user, app_db_mapping)

	return render(request, 'Home/home.html', {'userStats': userStats})



def getUserStatistics(userId, app_db_mapping):
	dict_userStats = dict()

	for appName in app_db_mapping:
		dict_userStats[appName] = dict()
		appClass = __import__(appName + ".models")

		try:
			if appClass.models.User.objects.filter(userId=userId).count() > 0:
				userObj = appClass.models.User.objects.get(userId=userId)
				projObjs = appClass.models.Project.objects.filter(user=userObj)
				dict_userStats[appName]['numProjects'] = projObjs.count()
				dict_userStats[appName]['numIsolates'] = appClass.models.Isolate.objects.filter(
                project__in=projObjs).count()
		except Exception as e:
			dict_userStats[appName]['numProjects'] = 0
			dict_userStats[appName]['numIsolates'] = 0
			sys.stderr.write(str(e))
		else:
			pass
		finally:
			pass

	return dict_userStats
