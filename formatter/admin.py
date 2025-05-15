from django.contrib import admin
from .models import Template, FormattedCV

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'default')

@admin.register(FormattedCV)
class FormattedCVAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'created_at')
