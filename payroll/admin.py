import logging

from django.contrib import admin

from .models import Payment, PayRecordRegister, PayRun, PayRunStatusChoices
from payees.utils import restrict_queryset_by_group
from .alerts import (approve_payrun_action, reject_payrun_action,
                     run_payrun_action, check_previous_month_payrun,
                     check_if_can_create_new_payrun, verify_existing_payrun,
                     is_payrun_rejected_or_exists)

logger = logging.getLogger(__name__)


# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payee", "label"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PayRunAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'status', 'created_by')
    list_filter = ('status', 'month', 'year')
    search_fields = ('status', 'month', 'year')
    readonly_fields = ('status', 'created_at')
    ordering = ['-created_at']
    actions = ['run_payrun', 'approve_payrun', 'reject_payrun' ]

    def save_model(self, request, obj, form, change):
        """
        To handle the creation of a new payrun entry when there is no
        existing entry or if the existing entry has a status of Rejected.
        """
        if not obj.pk:
            if is_payrun_rejected_or_exists(self, obj):
                obj.created_by = request.user
                obj.status = PayRunStatusChoices.DUE
                super().save_model(request, obj, form, change)
                return

            if not verify_existing_payrun(self, obj, request):
                return

            if not check_previous_month_payrun(self, obj, request):
                return

            if not check_if_can_create_new_payrun(self, obj, request):
                return

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
