from django.db import models

class Template(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='templates/')
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class FormattedCV(models.Model):
    original_file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='results/')
    candidate_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'CV {self.candidate_name}'
