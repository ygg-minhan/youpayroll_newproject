import logging
from django.contrib import admin
from .models import (Payee, TDS, Payment, BankDetails, PayRecordRegister,
                     PayRecord, BankDetailsAck, PayRun)
from employees.utils import restrict_queryset_by_group
from .tasks import fetch_details

logger = logging.getLogger(__name__)


class PayeeAdmin(admin.ModelAdmin):
    list_display = ["hrm_id", "full_name", "tds_type", "status"]
    readonly_fields = ["full_name", "email", "pan_no", "address",
                       "date_of_joining"]
    ordering = ("status",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        fetch_details.delay(obj.hrm_id)

    def delete_queryset(self, request, queryset):
        queryset.update(is_deleted=True)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        qs = queryset.filter(is_deleted=False)
        return restrict_queryset_by_group(qs, request.user)


class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ["payee", "bank_name", "account_type",
                    "payee_acknowledgement"]
    readonly_fields = ('payee_acknowledgement',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payee", "label"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PayRecordAdmin(admin.ModelAdmin):
    list_display = ["payee", "month"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PayRunAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'status')
    list_filter = ('status', 'month', 'year')
    search_fields = ('status', 'month', 'year')


admin.site.register(TDS)
admin.site.register(Payee, PayeeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BankDetails, BankDetailsAdmin)
admin.site.register(BankDetailsAck)
admin.site.register(PayRecordRegister)
admin.site.register(PayRecord, PayRecordAdmin)
admin.site.register(PayRun, PayRunAdmin)
