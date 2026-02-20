from django.contrib import admin
from .models import Payee, BankDetail, BankDetailAcknowledgement

@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ('payee', 'bank_name', 'account_number', 'ifsc_code')
    list_filter = ('bank_name',)
    search_fields = ('payee__name', 'account_number')

@admin.register(BankDetailAcknowledgement)
class BankDetailAcknowledgementAdmin(admin.ModelAdmin):
    list_display = ('bank_detail', 'acknowledged_by', 'acknowledged_at', 'status')
    list_filter = ('status', 'acknowledged_at')
