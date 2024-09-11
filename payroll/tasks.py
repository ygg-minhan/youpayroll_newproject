import logging

from celery import shared_task

from .models import PayRun, Payment, PayRunStatusChoices, PayRecordRegister
from payees.models import Payee, BankDetails

# For getting the named logger
logger = logging.getLogger('celery_debug')


@shared_task
def run_pay_run_task(payrun_id):

    logger.info('Starting task with pay_run_id: %s', payrun_id)

    pay_run = PayRun.objects.get(id=payrun_id)
    # Retrieve payees
    payees = Payee.objects.filter(
        status='active', bankdetails__payee_acknowledgement=True).distinct()

    pay_run.status = PayRunStatusChoices.IN_PROGRESS
    pay_run.save()

    logger.info('PayRun status updated to: %s', pay_run.status)

    for payee in payees:
        logger.info('Processing payee: %s', payee)

        bank_details = BankDetails.objects.get(payee=payee)

        total_amount = Payment.objects.filter(payee=payee)

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
        )

        pay_run.status = PayRunStatusChoices.COMPLETED
        pay_run.save()
        logger.info('PayRecordRegister created for payee: %s', payee)


