from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
import os
import tempfile
import shutil
import time
import dotenv
from pathlib import Path
import base64
import requests
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session
from django.utils import timezone
from django.http import JsonResponse

# Cargar variables de entorno desde el archivo .env
env_path = Path('.') / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

from .forms import CVUploadForm
from .models import FormattedCV
from .utils import process_cv

# Obtener la clave API de OpenAI desde variables de entorno
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# -------- VISTAS PARA FORMATEO DE CVs --------
def index(request):
    # Si el usuario no está autenticado, redirigir al login
    if not request.session.get('cognito_user'):
        return redirect('login_view')
    
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Obtener archivos
                cv_file = request.FILES['cv_file']
                template_file = request.FILES['template_file']
                
                # Guardar los archivos temporalmente
                temp_dir = tempfile.mkdtemp()
                
                # Guardar el CV
                cv_path = os.path.join(temp_dir, cv_file.name)
                with open(cv_path, 'wb+') as destination:
                    for chunk in cv_file.chunks():
                        destination.write(chunk)
                
                # Guardar la plantilla
                template_path = os.path.join(temp_dir, template_file.name)
                with open(template_path, 'wb+') as destination:
                    for chunk in template_file.chunks():
                        destination.write(chunk)
                
                # Procesar el CV
                print("Iniciando procesamiento de CV...")
                result = process_cv(
                    input_file_path=cv_path,
                    template_path=template_path,
                    api_key=OPENAI_API_KEY,
                    model="o4-mini"
                )
                print("Procesamiento completado.")
                
                if result['success']:
                    # Guardar el registro en la base de datos
                    formatted_cv = FormattedCV()
                    # Cambio aquí: usar cv_file en lugar de original_file
                    formatted_cv.cv_file.save(
                        os.path.basename(cv_path),
                        open(cv_path, 'rb')
                    )
                    
                    # Guardar el archivo procesado
                    output_basename = os.path.basename(result['output_path'])
                    formatted_cv.processed_file.save(
                        output_basename,
                        open(result['output_path'], 'rb')
                    )
                    
                    formatted_cv.candidate_name = result.get('name', 'Sin nombre')
                    formatted_cv.save()
                    
                    # Agregar mensaje de éxito y redirigir al historial
                    messages.success(
                        request, 
                        f"✅ CV procesado exitosamente para {result.get('name', 'el candidato')}. "
                        f"Puedes descargarlo desde el historial."
                    )
                    
                    # Limpiar archivos temporales
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass
                    
                    # Redirigir al historial en lugar de descargar directamente
                    return redirect('list_cvs')
                else:
                    # Limpiar archivos temporales
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass
                    
                    messages.error(request, f"Error: {result['error']}")
            except Exception as e:
                # Manejar cualquier excepción inesperada
                messages.error(request, f"Error inesperado: {str(e)}")
                import traceback
                traceback.print_exc()
    else:
        form = CVUploadForm()
    
    # Obtener información del usuario de la sesión
    user_info = request.session.get('cognito_user', {})
    
    return render(request, 'formatter/index.html', {
        'form': form,
        'user_info': user_info
       
    })

def list_cvs(request):
    # Si el usuario no está autenticado, redirigir al login
    if not request.session.get('cognito_user'):
        return redirect('login_view')
    
    cvs = FormattedCV.objects.all().order_by('-created_at')
    # Modificar el formato de fecha aquí
    for cv in cvs:
        # Formato para Chile: DD/MM/YYYY HH:MM
        cv.formatted_date = cv.created_at.strftime('%d/%m/%Y %H:%M')
    
    # Obtener información del usuario de la sesión
    user_info = request.session.get('cognito_user', {})
    
    return render(request, 'formatter/list_cvs.html', {
        'cvs': cvs,
        'user_info': user_info,
        'login_page': True,
        
    })

def download_cv(request, cv_id):
    # Si el usuario no está autenticado, redirigir al login
    if not request.session.get('cognito_user'):
        return redirect('login_view')
    
    try:
        cv = FormattedCV.objects.get(id=cv_id)
        
        # Marcar como descargado
        if not cv.downloaded:
            cv.downloaded = True
            from django.utils import timezone  # Agregar este import arriba del archivo
            cv.downloaded_at = timezone.now()
            cv.save()
        
        return FileResponse(
            open(cv.processed_file.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(cv.processed_file.name)
        )
    except FormattedCV.DoesNotExist:
        messages.error(request, "CV no encontrado")
        return redirect('list_cvs')
    

#autenticacion

def get_oidc_config():
    """Obtiene la configuración de OpenID Connect desde el endpoint de descubrimiento"""
    try:
        resp = requests.get(settings.COGNITO['DISCOVERY_URL'], timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error obteniendo configuración OIDC: {e}")
        # En caso de error, proporcionar URLs conocidas para evitar fallos
        return {
            'authorization_endpoint': f"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_lP9Tp4Io5/oauth2/authorize",
            'token_endpoint': f"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_lP9Tp4Io5/oauth2/token",
            'userinfo_endpoint': f"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_lP9Tp4Io5/oauth2/userInfo",
            'end_session_endpoint': f"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_lP9Tp4Io5/logout",
        }

def login_view(request):
    """Vista para mostrar la página de inicio de sesión"""
    if 'cognito_user' in request.session:
        return redirect('index')
    
    return render(request, 'formatter/login.html', {'login_page': True})

def initiate_login(request):
    """Inicia el proceso de login con AWS Cognito"""
    config = get_oidc_config()
    session = OAuth2Session(
        client_id=settings.COGNITO['CLIENT_ID'],
        client_secret=settings.COGNITO['CLIENT_SECRET'],
        scope='openid email',
        redirect_uri=settings.COGNITO['REDIRECT_URI'],
    )
    
    uri, state = session.create_authorization_url(config['authorization_endpoint'])
    request.session['state'] = state
    return redirect(uri)

def authorize(request):
    """Procesa el código de autorización recibido de AWS Cognito"""
    try:
        config = get_oidc_config()
        state = request.session.get('state')
        
        session = OAuth2Session(
            client_id=settings.COGNITO['CLIENT_ID'],
            client_secret=settings.COGNITO['CLIENT_SECRET'],
            scope='openid email',
            redirect_uri=settings.COGNITO['REDIRECT_URI'],
            state=state,
        )
        
        token = session.fetch_token(
            config['token_endpoint'],
            authorization_response=request.build_absolute_uri(),
            client_secret=settings.COGNITO['CLIENT_SECRET'],
        )
        
        request.session['access_token'] = token.get('access_token')
        request.session['refresh_token'] = token.get('refresh_token', None)
        
        # Obtener información del usuario
        userinfo = session.get(config['userinfo_endpoint']).json()
        
        # Guardar información en la sesión
        request.session['cognito_user'] = userinfo
        
        # Redirigir al dashboard
        messages.success(request, f"Bienvenido, {userinfo.get('email', 'usuario')}!")
        return redirect('index')
        
    except Exception as e:
        error_message = f"Error en el proceso de autenticación: {str(e)}"
        print(error_message)  # Para depuración
        return render(request, 'formatter/login.html', {'error_message': error_message, 'login_page': True})

def logout_view(request):
    """Cierra la sesión del usuario tanto en la aplicación como en AWS Cognito"""
    try:
        config = get_oidc_config()
        
        # Construir la URL de logout de Cognito
        logout_url = (
            f"{config['end_session_endpoint']}"
            f"?client_id={settings.COGNITO['CLIENT_ID']}"
            f"&logout_uri={urllib.parse.quote(settings.COGNITO['LOGOUT_URI'])}"
        )
        
        # Limpiar la sesión
        request.session.flush()
        
        # Cerrar sesión de Django
        logout(request)
        
        # Redirigir a la URL de logout de Cognito
        return redirect(logout_url)
        
    except Exception as e:
        print(f"Error en el proceso de logout: {str(e)}")
        
        # Si hay un error, al menos limpiar la sesión local
        request.session.flush()
        logout(request)
        
        # Redirigir a la página de login
        return redirect('login_view')
    
    #funcion para desmarcar una vez descargado el cv
def mark_as_downloaded(request, cv_id):
    if request.method == 'POST':
        try:
            cv = FormattedCV.objects.get(id=cv_id)
            cv.downloaded = True
            cv.downloaded_at = timezone.now()
            cv.save()
            return JsonResponse({'success': True})
        except FormattedCV.DoesNotExist:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})