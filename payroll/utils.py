from django.contrib import messages


def check_single_payrun_selection(queryset, modeladmin, request):
    """
   Checks if exactly one item is selected in the queryset.
   Displays an error message if not.
   Returns True if exactly one item is selected, False otherwise.
   """
    if queryset.count() != 1:
        modeladmin.message_user(
            request,
            "Please select only one payrun entry at a time. Multiple "
            "selections are not allowed to ensure accurate processing.",
            level=messages.ERROR
        )
        return False
    return True


def check_latest_payrun(modeladmin, request, selected_payrun, latest_payrun):
    """
    Ensure that a selected payrun entry is the most recent one before
    proceeding with an action in an administrative interface.
    """
    if selected_payrun != latest_payrun:
        modeladmin.message_user(
            request,
            "To proceed, please select the most recent payrun entry.",
            level=messages.ERROR
        )
        return False
    return True
