from django.contrib import messages

from .models import PayRun, PayRunStatusChoices, Payee
from .tasks import run_pay_run_task
from .utils import check_single_selection, check_latest_payrun


def approve_payrun_action(modeladmin, request, queryset):
    """
    Approve the selected payrun entry.
    """
    selected_payrun = queryset.first()
    latest_payrun = PayRun.objects.all().last()

    if not check_single_selection(queryset, modeladmin, request):
        return

    if not check_latest_payrun(modeladmin, request, selected_payrun,
                               latest_payrun):
        return

    if latest_payrun.status == PayRunStatusChoices.COMPLETED:
        latest_payrun.status = PayRunStatusChoices.APPROVED
        latest_payrun.save()
        modeladmin.message_user(request,
                                "Pay records have been approved successfully.",
                                level=messages.SUCCESS)
    else:
        modeladmin.message_user(request,
                                "Entries can only be approved if their status "
                                "is 'Completed'. To update the status and "
                                "enable approval, please run the "
                                "pay run process.", level=messages.ERROR)


def reject_payrun_action(modeladmin, request, queryset):
    """
    Reject the selected payrun entry.
    """
    selected_payrun = queryset.first()
    latest_payrun = PayRun.objects.all().last()

    if not check_single_selection(queryset, modeladmin, request):
        return

    if not check_latest_payrun(modeladmin, request, selected_payrun,
                               latest_payrun):
        return

    if (latest_payrun.status == PayRunStatusChoices.COMPLETED or
            latest_payrun.status == PayRunStatusChoices.APPROVED):

        latest_payrun.status = PayRunStatusChoices.REJECTED
        latest_payrun.save()

        modeladmin.message_user(request, "The payrun entry has been rejected.",
                                level=messages.SUCCESS)
    else:
        modeladmin.message_user(request,
                                "Entries can only be rejected if their status "
                                "is 'Completed' or 'Approved.' To update the "
                                "status and enable rejection, please run the "
                                "pay run process.",
                                level=messages.ERROR)


def run_payrun_action(modeladmin, request, queryset):
    """
    Queue a Celery task to process the selected payrun entry.
    """
    latest_payrun = PayRun.objects.all().last()
    selected_payrun = queryset.first()

    if not check_single_selection(queryset, modeladmin, request):
        return

    if not check_latest_payrun(modeladmin, request, selected_payrun,
                               latest_payrun):
        return

    if latest_payrun.status == PayRunStatusChoices.APPROVED:
        modeladmin.message_user(request,
                                "The selected pay run has already been "
                                "approved.", level=messages.ERROR)

    elif latest_payrun.status == PayRunStatusChoices.COMPLETED:
        modeladmin.message_user(request,
                                "The pay run has been completed. To proceed, "
                                "please choose either 'Approve' or 'Reject'.",
                                level=messages.ERROR)

    elif latest_payrun.status == PayRunStatusChoices.IN_PROGRESS:
        modeladmin.message_user(request,
                                "We’re currently syncing your pay record. "
                                "Please hold on while we update your "
                                "information.", level=messages.SUCCESS)

    elif latest_payrun.status == PayRunStatusChoices.REJECTED:
        modeladmin.message_user(request,
                                "The pay records have been rejected."
                                "Please initiate a new pay run to proceed.",
                                level=messages.ERROR)

    elif latest_payrun.status == PayRunStatusChoices.DUE:

        payees = Payee.objects.filter(
            status='active',
            bankdetails__payee_acknowledgement=True).distinct()

        if not payees.exists():
            modeladmin.message_user(request,
                                    "No active payees found with acknowledged "
                                    "bank details. Please check and try again",
                                    level=messages.ERROR)

            latest_payrun.status = PayRunStatusChoices.REJECTED
            latest_payrun.save()
        else:
            run_pay_run_task.delay(latest_payrun.id)

            modeladmin.message_user(request,
                                    "Your pay run has been successfully "
                                    "started and is currently being processed.",
                                    level=messages.SUCCESS)


def is_payrun_rejected_or_exists(self, obj):
    """
    Checks whether the latest payrun entry has been rejected or if there are
    no existing payrun entries in the database.
    """
    if not PayRun.objects.exists():
        return True

    latest_payrun = PayRun.objects.all().last()
    return (latest_payrun.status == PayRunStatusChoices.REJECTED and
            latest_payrun.month == obj.month and
            latest_payrun.year == obj.year)


def verify_existing_payrun(self, obj, request):
    """
    Checks whether a payrun entry already exists for a given month and year
    and verifies the status of the latest payrun entry. If an existing payrun
    is found that is not rejected, it sends an error message to the user.
    """
    existing_pay_runs = PayRun.objects.filter(
        month=obj.month, year=obj.year
    ).order_by('-id')

    if existing_pay_runs.exists():
        latest_payrun = existing_pay_runs.first()
        if latest_payrun.status != PayRunStatusChoices.REJECTED:
            messages.set_level(request, messages.ERROR)
            self.message_user(request,
                              f"Error: A Pay Run already exists for "
                              f"{latest_payrun.get_month_display()} - "
                              f"{latest_payrun.year} with status"
                              f" {latest_payrun.status}.",
                              messages.ERROR)
            return False
    return True


def check_previous_month_payrun(self, obj, request):
    """
    Verifies the existence of a payrun entry for the previous month before
    allowing the creation of a new payrun entry for the current month.
    """
    previous_month = obj.month - 1
    previous_year = obj.year
    if previous_month == 0:
        previous_month = 12
        previous_year -= 1

    previous_pay_run_exists = PayRun.objects.filter(
        month=previous_month, year=previous_year
    ).exists()

    if not previous_pay_run_exists:
        messages.set_level(request, messages.ERROR)
        self.message_user(request,
                          f"A Pay Run for the previous month "
                          f"{previous_month} / {previous_year} "
                          f"must exist before creating a new one.",
                          messages.ERROR)
        return False
    return True


def check_if_can_create_new_payrun(self, obj, request):
    """
    Determines whether a new payrun entry can be created based on the status
    of the latest payrun entry and its relationship to the previous month.
    """
    latest_payrun = PayRun.objects.all().last()
    previous_month = obj.month - 1
    previous_year = obj.year
    if previous_month == 0:
        previous_month = 12
        previous_year -= 1

    if latest_payrun.status == PayRunStatusChoices.REJECTED:
        if previous_month != obj.month or previous_year != obj.year:
            messages.set_level(request, messages.ERROR)
            self.message_user(request,
                              f"A Pay Run for the previous "
                              f"month {previous_month} / {previous_year} "
                              f"was rejected. You can only create a "
                              f"new Pay Run for the rejected month.",
                              messages.ERROR)
            return False
    elif (latest_payrun.status == PayRunStatusChoices.DUE or
          latest_payrun.status == PayRunStatusChoices.COMPLETED):
        messages.set_level(request, messages.ERROR)
        self.message_user(request,
                          f"There's already a Pay Run for "
                          f"{previous_month} / {previous_year}. "
                          f"Please 'approve' or 'reject'  the existing "
                          f"Pay Run before creating a new one.",
                          messages.ERROR)
        return False
    return True
