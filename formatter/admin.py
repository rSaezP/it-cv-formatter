# formatter/admin.py
from django.contrib import admin
from .models import FormattedCV

@admin.register(FormattedCV)
class FormattedCVAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'created_at')
    search_fields = ('candidate_name',)
    readonly_fields = ('created_at',)
    
