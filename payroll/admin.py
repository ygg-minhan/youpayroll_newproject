from django.contrib import admin
from .models import PayRun, Payment, PayRecordRegister, Form16, Form16Entry

@admin.register(PayRun)
class PayRunAdmin(admin.ModelAdmin):
    list_display = ('run_date', 'status')
    list_filter = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payee', 'amount', 'payment_date', 'pay_run')
    list_filter = ('pay_run', 'payment_date')
    search_fields = ('payee__name', 'reference_number')

@admin.register(PayRecordRegister)
class PayRecordRegisterAdmin(admin.ModelAdmin):
    list_display = ('pay_run', 'generated_at')

@admin.register(Form16)
class Form16Admin(admin.ModelAdmin):
    list_display = ('payee', 'financial_year')
    list_filter = ('financial_year',)
    search_fields = ('payee__name',)

@admin.register(Form16Entry)
class Form16EntryAdmin(admin.ModelAdmin):
    list_display = ('form16', 'section', 'amount')
    list_filter = ('form16__financial_year',)
