from django import forms

class CVUploadForm(forms.Form):
    cv_file = forms.FileField(
        label='Seleccionar CV (PDF o DOCX)', 
        help_text='Formatos aceptados: PDF, DOCX',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    template_file = forms.FileField(
        label='Seleccionar plantilla (DOCX)', 
        help_text='Formato aceptado: DOCX',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
