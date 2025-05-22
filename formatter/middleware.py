# formatter/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de URLs que no requieren autenticación
        exempt_urls = [
            reverse('login_view'),  # Página de login
            reverse('login'),       # Proceso de login
            reverse('authorize'),   # Callback de autorización
            # Añade aquí cualquier otra URL que no requiera autenticación
        ]
        
        # URLs que contienen "admin" también están exentas (para acceder al admin de Django)
        if '/admin/' in request.path_info:
            return self.get_response(request)
        
        # Verificar si el usuario está autenticado o si la URL está exenta
        if not request.session.get('cognito_user') and request.path_info not in exempt_urls:
            # Usuario no autenticado y URL no exenta, redirigir al login
            return redirect('login_view')
            
        response = self.get_response(request)
        return response