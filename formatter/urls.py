from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal muestra el login
    path('', views.login_view, name='login_view'),
    
    # Ruta para el index (ahora accesible en /dashboard/)
    path('dashboard/', views.index, name='index'),
    
    # Otras rutas existentes
    path('list/', views.list_cvs, name='list_cvs'),
    path('download/<int:cv_id>/', views.download_cv, name='download_cv'),
    
    # Rutas de autenticación
    path('initiate-login/', views.initiate_login, name='login'),
    path('authorize/', views.authorize, name='authorize'),
    path('logout/', views.logout_view, name='logout'),

    # Ruta para la vista de descarga
    path('mark-downloaded/<int:cv_id>/', views.mark_as_downloaded, name='mark_downloaded'),
]
