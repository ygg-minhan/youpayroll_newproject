import logging

from celery import shared_task
from decimal import Decimal

from .models import (PayRun, Payment, PayRunStatusChoices, PayRecordRegister)
from payees.models import Payee, BankDetails

# For getting the named logger
logger = logging.getLogger('celery_debug')


@shared_task
def run_pay_run_task(payrun_id):
    logger.info('Starting task with pay_run_id: %s', payrun_id)

    pay_run = PayRun.objects.get(id=payrun_id)
    if pay_run.status == PayRunStatusChoices.DUE:
        # Retrieve payees
        payees = Payee.objects.filter(
            status='active', bankdetails__payee_acknowledgement=True)

        pay_run.status = PayRunStatusChoices.IN_PROGRESS
        pay_run.save()
        logger.info('PayRun status updated to: %s', pay_run.status)

        for payee in payees:
            logger.info('Processing payee: %s', payee)

            try:
                bank_details = BankDetails.objects.get(payee=payee)
                total_amount = Payment.objects.get(payee=payee)

            except BankDetails.DoesNotExist:
                bank_details = None
                print("Bank details not found for this payee.")

            except Payment.DoesNotExist:
                total_amount = None
                print("Payment not found for this payee.")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

            # Create PayRecordRegister entry
            PayRecordRegister.objects.create(
                pay_run=pay_run,
                amount=total_amount.amount,
                payee=payee,
                bank_name=bank_details.bank_name,
                account_number=bank_details.account_no,
                account_holder_name=bank_details.account_holder_name,
                account_type=bank_details.account_type,
                ifsc_code=bank_details.ifsc_code,
                micr_code=bank_details.micr_code,
                swift_code=bank_details.swift_code,
                branch_address=bank_details.branch_address,
                tds_percentage=payee.tds_type.tds_percentage if payee.tds_type else None,
                gross_amount=total_amount.amount,
            )

        pay_run.status = PayRunStatusChoices.COMPLETED
        pay_run.save()
        logger.info('PayRecordRegister created for payee: %s', )


def net_income_salary_calculation(pay_run_id):
    """
    Calculate take-home salary for all employees in a given PayRun.
    """
    try:
        """
        Get the pay_run data if their status is COMPLETED
        """
        pay_run = PayRun.objects.get(id=pay_run_id, status=PayRunStatusChoices.COMPLETED)
    except PayRun.DoesNotExist:
        logger.warning(f"PayRun with id={pay_run_id} and status=COMPLETED not "
                 f"found.")
        return

    # Get all PayRecordRegister entries linked to this PayRun
    pay_records = PayRecordRegister.objects.filter(pay_run=pay_run)

    if not pay_records.exists():
        logger.warning(f"No PayRecordRegister entries found for PayRun ID"
                f" {pay_run_id}.")
        return
    """
    Update the take home salary of the employees , if their pay_run status 
    is COMPLETED
    """
    for pay_record in pay_records:

        if pay_record.gross_amount is None or pay_record.gross_amount <= 0:
            # Print statement to identify the payee
            logger.warning(
                f"Payee with ID={pay_record.id} (Payee:"
                f" {pay_record.payee.hrm_id}) does not have a valid "
                f"gross_amount: {pay_record.gross_amount}.")
            continue
        tds_percentage = Decimal(str(pay_record.tds_percentage or 0))  # Safe default to 0
        tds_amount = (pay_record.gross_amount * tds_percentage) / Decimal('100')
        net_income = pay_record.gross_amount - tds_amount

        pay_record.net_income = net_income
        pay_record.save()
