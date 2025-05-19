from django import forms

class CVUploadForm(forms.Form):
    """
    Formulario para subir un CV y una plantilla
    """
    cv_file = forms.FileField(
        label="Archivo CV",
        help_text="Formatos aceptados: PDF, DOCX",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.doc'})
    )
    
    template_file = forms.FileField(
        label="Archivo de plantilla",
        help_text="Formato aceptado: DOCX",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.docx'})
    )
    
    def clean_cv_file(self):
        """
        Validar que el archivo CV tenga un formato aceptado
        """
        cv_file = self.cleaned_data.get('cv_file')
        if cv_file:
            filename = cv_file.name.lower()
            if not (filename.endswith('.pdf') or filename.endswith('.docx') or filename.endswith('.doc')):
                raise forms.ValidationError("Por favor, sube un archivo PDF o DOCX")
        return cv_file
    
    def clean_template_file(self):
        """
        Validar que el archivo de plantilla tenga un formato aceptado
        """
        template_file = self.cleaned_data.get('template_file')
        if template_file:
            filename = template_file.name.lower()
            if not filename.endswith('.docx'):
                raise forms.ValidationError("Por favor, sube un archivo DOCX")
        return template_file