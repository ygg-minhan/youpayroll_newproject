import logging

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from payees.utils import restrict_queryset_by_group
from .models import Payment, PayRecordRegister, PayRun
from .alerts import (approve_payrun_action, reject_payrun_action,
                     run_payrun_action, is_payrun_exists)
from .forms import PayRunForm

logger = logging.getLogger(__name__)


# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payee", "label"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PayRunAdmin(admin.ModelAdmin):
    list_display = ('display_month_name', 'year', 'status', 'created_by')
    list_filter = ('status', 'month', 'year')
    search_fields = ('status', 'get_month_name', 'year')
    readonly_fields = ('status', 'created_at')
    ordering = ['-created_at']
    actions = ['run_payrun', 'approve_payrun', 'reject_payrun']
    form = PayRunForm

    def add_view(self, request, form_url='', extra_context=None):
        if is_payrun_exists(request):
            return redirect(reverse('admin:payroll_payrun_changelist'))
        return super().add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if change == False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def approve_payrun(self, request, queryset):
        approve_payrun_action(self, request, queryset)

    approve_payrun.short_description = 'Approve selected payrun'

    def reject_payrun(self, request, queryset):
        reject_payrun_action(self, request, queryset)

    reject_payrun.short_description = 'Reject selected payrun'

    def run_payrun(self, request, queryset):
        run_payrun_action(self, request, queryset)

    run_payrun.short_description = 'Run selected payrun'


class PayRecordRegisterAdmin(admin.ModelAdmin):
    readonly_fields = ('payee', 'amount', 'pay_run', 'tds_percentage',
                       'bank_name', 'account_number', 'account_holder_name',
                       'account_type', 'ifsc_code', 'micr_code',
                       'swift_code', 'branch_address')
    list_filter = ['pay_run__status', 'pay_run__month', 'pay_run__year']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PayRecordRegister, PayRecordRegisterAdmin)
admin.site.register(PayRun, PayRunAdmin)
