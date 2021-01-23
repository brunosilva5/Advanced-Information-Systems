"""
Register SWOTAnalysis model in django admin interface
"""
from django.contrib import admin
from .models import SWOTAnalysis


@admin.register(SWOTAnalysis)
class SWOTAnalysisAdmin(admin.ModelAdmin):
    pass