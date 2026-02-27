
from django_saas.core.base.admin import BaseAdmin
from django.contrib import admin

admin.site.site_title = 'Clinica'
admin.site.index_title = 'Clinica'

def all_fields(model):
    return [field.name for field in model._meta.fields]

