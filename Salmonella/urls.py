from django.conf.urls import url

from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
	# url(r'^session/(?P<pk>[^/]+)$', views.sessionInfo.page, name='session_var'),
	url(r'^$', views.index.page, name='index'),


	url(r'^projects$', login_required(views.cbv.projectList.ProjectListView.as_view()), name="project_list"),
	url(r'^project-create$', login_required(views.cbv.projectCreate.CreateProjectView.as_view()), name='project_create'),
    url(r'^project-(?P<pk>\d+)-edit$', login_required(views.cbv.projectEdit.ProjectUpdateView.as_view()), name='project_edit'),
	url(r'project-(?P<pk>\d+)-detail$', login_required(views.cbv.projectDetail.ProjectDetailView.as_view()), name='project_detail'),

    url(r'project-(?P<pk>\d+)-delete$', login_required(views.cbv.projectDelete.ProjectDeleteView.as_view()), name='project_delete'),
	# url(r'^isolate-(?P<pk>\d+)-detail$', login_required(views.cbv.isolateDetail.IsolateDetailView.as_view()), name="isolate_detail"), TODO: rename

	url(r'^isolate-list$', views.isolateList.page, name='isolate_list'),
	url(r'^isolate-create$', login_required(views.isolateCreate.page), name='isolate_create'),
    url(r'^isolate-(?P<pk>\d+)-edit$', login_required(views.isolateEdit.page), name='isolate_edit'),
    url(r'isolate-(?P<pk>\d+)-delete$', login_required(views.cbv.isolateDelete.IsolateDeleteView.as_view()), name='isolate_delete'),
	url(r'^isolate-(?P<pk>\d+)-detail$', views.isolateDetail.page, name="isolate_detail"),


	url(r'^initial-isolates$', views.ajax.initialIsolates.page, name='initial_isolates'),
	url(r'^initial-projectIsolates$', login_required(views.ajax.initialProjectIsolates.page), name='initial_projectIsolates'),

	url(r'^search-projectDetail$', views.ajax.searchProjectDetail.page, name='search_projectDetail'),
	url(r'^search-isolateList$', views.ajax.searchIsolateList.page, name='search_isolateList'),
	url(r'^search-isolateDetail$', views.ajax.searchIsolateDetail.page, name='search_isolateDetail'),


	url(r'^top-st$', views.ajax.topStSummary.page, name='topStSummary'),
	# url(r'^order-by$', views.ajax.orderBy_router.page, name='order_by'),





    # url(r'^create-isolate$', login_required(views.cbv.createIsolate.CreateIsolateView.as_view()), name='create_isolate'),
    # url(r'^create-isolate$', login_required(views.createIsolate.page), name='create_isolate'),
	# url(r'^isolate-(?P<pk>\d+)-edit$', login_required(views.cbv.editIsolate.IsolateUpdateView.as_view()), name='edit_isolate'),

]
