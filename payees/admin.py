import logging
from django.contrib import admin

from payroll.admin import Form16Inline
from youpayroll.admin_mixins import PayeeRestrictAdmin
from .models import (Payee, BankDetails, BankDetailsAck)
from .utils import restrict_queryset_by_group
from .tasks import fetch_details

logger = logging.getLogger(__name__)


class PayeeAdmin(admin.ModelAdmin):
    inlines = [Form16Inline]
    list_display = ["hrm_id", "full_name", "tds_type", "status", "user"]
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

        if request.user.is_superuser:
            return restrict_queryset_by_group(qs, request.user)

        # Non-superusers only see their own Payee record
        return restrict_queryset_by_group(qs.filter(user=request.user),
                                          request.user)


class BankDetailsAdmin(PayeeRestrictAdmin):
    list_display = ["payee", "bank_name", "account_type",
                    "payee_acknowledgement"]
    readonly_fields = ('payee_acknowledgement',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class BankDetailsAckAdmin(PayeeRestrictAdmin):
    list_display = ['payee', 'uploaded_date']


admin.site.register(Payee, PayeeAdmin)
admin.site.register(BankDetails, BankDetailsAdmin)
admin.site.register(BankDetailsAck, BankDetailsAckAdmin)
