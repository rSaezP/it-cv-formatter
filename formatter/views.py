from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.conf import settings
import os
import tempfile
import shutil
import time
import dotenv
from pathlib import Path

# Cargar variables de entorno desde el archivo .env
env_path = Path('.') / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

from .forms import CVUploadForm
from .models import FormattedCV
from .utils import process_cv

# Obtener la clave API de OpenAI desde variables de entorno
OPENAI_API_KEY = "TU_CLAVE_API_AQUI"

def index(request):
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
                    formatted_cv.original_file.save(
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
                    
                    # Preparar la respuesta de descarga
                    response = FileResponse(
                        open(formatted_cv.processed_file.path, 'rb'),
                        as_attachment=True,
                        filename=output_basename
                    )
                    
                    # Limpiar archivos temporales
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass
                    
                    return response
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
    
    return render(request, 'formatter/index.html', {'form': form})

def list_cvs(request):
    cvs = FormattedCV.objects.all().order_by('-created_at')
    return render(request, 'formatter/list.html', {'cvs': cvs})

def download_cv(request, cv_id):
    try:
        cv = FormattedCV.objects.get(id=cv_id)
        return FileResponse(
            open(cv.processed_file.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(cv.processed_file.name)
        )
    except FormattedCV.DoesNotExist:
        messages.error(request, "CV no encontrado")
        return redirect('list_cvs')
