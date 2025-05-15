from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_cvs, name='list_cvs'),
    path('download/<int:cv_id>/', views.download_cv, name='download_cv'),
]
