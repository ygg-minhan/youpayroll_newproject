import logging

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from payees.utils import restrict_queryset_by_group
from .models import (Payment, PayRecordRegister, PayRun,
                     PayRunStatusChoices, Form16, Form16Entries)
from .alerts import (approve_payrun_action, reject_payrun_action,
                     run_payrun_action, is_payrun_exists)
from .forms import PayRunForm
from .models import ComponentValue

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


class ComponentValueInline(admin.TabularInline):
    model = ComponentValue
    fields = ('component', 'value')
    can_delete = False
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Disable related buttons (add, view, change)
        component_field = formset.form.base_fields['component']
        component_field.widget.can_add_related = False
        component_field.widget.can_change_related = False
        component_field.widget.can_view_related = False

        # Disable fields if the PayRun status is 'APPROVED'
        if obj and obj.pay_run.status == PayRunStatusChoices.APPROVED:
            component_field.disabled = True
            formset.form.base_fields['value'].disabled = True

        return formset

    def has_add_permission(self, request, obj=None):
        # Disable add permission if PayRun status is 'APPROVED'
        if obj and obj.pay_run.status == PayRunStatusChoices.APPROVED:
            return False
        return super().has_add_permission(request, obj)


class PayRecordRegisterAdmin(admin.ModelAdmin):
    inlines = [ComponentValueInline]
    readonly_fields = ('payee', 'amount', 'pay_run', 'tds_percentage',
                       'bank_name', 'account_number', 'account_holder_name',
                       'account_type', 'ifsc_code', 'micr_code',
                       'swift_code', 'branch_address', 'gross_amount',)
    list_filter = ('pay_run__status', 'pay_run__month', 'pay_run__year')
    list_display = ('payee', 'amount', 'gross_amount', 'pay_run')
    actions = None  # Disable the delete action

    def has_delete_permission(self, request, obj=None):
        # Hide delete for all objects
        if obj:
            return False
        return super().has_delete_permission(request, obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        pay_record_register = form.instance

        # Calculate the total based on component operations (sum or subtract)
        total = pay_record_register.amount + sum(
            component_value.value if component_value.component.operation == 'sum'
            else -component_value.value
            for component_value in
            ComponentValue.objects.filter(pay_record=pay_record_register)
        )

        # Update gross_amount and save the instance
        pay_record_register.gross_amount = total
        pay_record_register.save()


class Forms16EntriesAdmin(admin.ModelAdmin):
    list_display = ('financial_year', 'form_16_link')
    list_filter = ('financial_year',)
    list_per_page = 20

    def form_16_link(self, obj):
        if obj.form_16:
            return format_html(
                "<a href='{}' target='_blank'>{}</a>",
                obj.form_16.url,
                obj.form_16.name.split('/')[-1]  # Show only filename
            )
        return "No File"

    form_16_link.short_description = "Form 16 File"


class Form16Inline(admin.TabularInline):  # or StackedInline
    model = Form16Entries
    fields = ['form_16_link', 'financial_year']
    readonly_fields = ['form_16_link', 'financial_year']
    extra = 0
    can_delete = False
    verbose_name = "Form16 PDF"
    verbose_name_plural = "Form16 PDFs"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('financial_year')

    def form_16_link(self, obj):
        if obj.form_16:
            return format_html(
                "<a href='{}' target='_blank'>{}</a>",
                obj.form_16.url,
                obj.form_16.name.split('/')[-1]  # Show only filename
            )
        return "No File"


class Forms16Admin(admin.ModelAdmin):
    list_display = ('financial_year', 'form_16_link', 'view_form_entries')

    def form_16_link(self, obj):
        if obj.form16_zip_file:
            return format_html(
                "<a href='{}' target='_blank'>{}</a>",
                obj.form16_zip_file.url,
                obj.form16_zip_file.name.split('/')[-1]  # Show only filename
            )
        return "No File"

    form_16_link.short_description = "Form 16 File"

    def view_form_entries(self, obj):
        """
        Generates a button that links to Form16Entries filtered by financial_year.
        """
        url = reverse(
            'admin:payroll_form16entries_changelist')
        url += f"?financial_year__id__exact={obj.id}"  # Filters by foreign key ID
        return format_html(
            '<a class="button" href="{}" style="background:#28a745; color:white; padding:4px 8px; border-radius:4px; text-decoration:none;">View Form Entries</a>',
            url)

    view_form_entries.short_description = "View Form Entries"


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PayRecordRegister, PayRecordRegisterAdmin)
admin.site.register(PayRun, PayRunAdmin)
admin.site.register(Form16, Forms16Admin)
admin.site.register(Form16Entries, Forms16EntriesAdmin)
