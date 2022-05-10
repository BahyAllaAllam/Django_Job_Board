from django.urls import path
from . import views
from . import api

app_name = 'job'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('add', views.add_job, name='add_job'),
    path('<str:slug>', views.job_detail, name='job_detail'),
    path('<str:slug>/update', views.update_job, name='update-job'),
    path('<str:slug>/delete', views.delete_job, name='delete-job'),
    path('job_applications/<int:id>', views.job_applications, name='job_applications'),
    path('change-language/', views.change_language, name='change_language'),
    path('api/job_list', api.JobListApi.as_view(), name='JobListApi'),
    path('api/job_detail/<int:id>', api.JobDetailApi.as_view(), name='JobDetailApi'),


]
'''
    path('api/jobs_list', api.job_list_api, name='job_list_api'),
    path('api/jobs_list/<int:id>', api.job_detail_api, name='job_detail_api'),
'''