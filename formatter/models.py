from django.db import models

class FormattedCV(models.Model):
    # Archivos - usar cv_file en lugar de original_file para coincidir con la base de datos
    cv_file = models.FileField(
        upload_to='uploads/',
        null=True,
        blank=True
    )
    
    processed_file = models.FileField(
        upload_to='results/',
        null=True,
        blank=True
    )
    
    # Metadatos
    candidate_name = models.CharField(
        max_length=255, 
        default="Candidato"
    )
    
    # Fechas
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f"CV de {self.candidate_name}"
    
    class Meta:
        verbose_name = "CV Formateado"
        verbose_name_plural = "CVs Formateados"