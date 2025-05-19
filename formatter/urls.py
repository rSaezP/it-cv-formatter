from django.urls import path
from . import views

urlpatterns = [
    # Página principal con formulario de subida
    path('', views.index, name='index'),
    
    # Lista de CVs procesados
    path('list/', views.list_cvs, name='list_cvs'),
    
    # Descargar CV procesado
    path('download/<int:cv_id>/', views.download_cv, name='download_cv'),
]
