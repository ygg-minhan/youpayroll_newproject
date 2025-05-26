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
                tds_percentage = Decimal(str(payee.tds_type.tds_percentage
                                             if payee.tds_type else 0))
                tds_amount = ((total_amount.amount * tds_percentage) /
                              Decimal('100'))

                total_net_income = total_amount.amount - tds_amount


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
                tds_percentage=tds_percentage,
                gross_amount=total_amount.amount,
                net_income=total_net_income,
            )

        pay_run.status = PayRunStatusChoices.COMPLETED
        pay_run.save()
        logger.info('PayRecordRegister created for payee: %s', )
