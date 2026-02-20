from django.contrib import admin
from .models import Component, TaxDeductedAtSource

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TaxDeductedAtSource)
class TaxDeductedAtSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')
    search_fields = ('name',)
