from decouple import config
from django.core.management.base import BaseCommand
from zohopeople.constants import (GRAND_TYPE, ZP_API_REDIR_URI,
                                  ZP_API_ATOKEN_DOM_URL)
from zohopeople.models import ZohoPeopleFormToken
from zohopeople.utils import tgeneration_call_api


def zoho_form_token_generation():
    """
    Generate Access token for sending data to Zoho People
    and Refresh token to generate new Access token. Store both
    tokens in DB.
    """
    tgeneration_data = {
        'grant_type': GRAND_TYPE,
        'client_id': config('ZOHOPEOPLE_CLIENT_ID'),
        'client_secret': config('ZOHOPEOPLE_CLIENT_SECRET'),
        'redirect_uri': ZP_API_REDIR_URI,
        'code': config('ZOHOPEOPLE_FORM_GRAND_TOKEN')
    }

    url = ZP_API_ATOKEN_DOM_URL
    # Send Post request for generating tokens.
    tgeneration_resp = tgeneration_call_api(url, tgeneration_data)

    if tgeneration_resp:
        # Convert response to json data.
        tgeneration_resp_val = tgeneration_resp.json()

        # Store tokens in the DB.
        tokens = ZohoPeopleFormToken(
            access_token=tgeneration_resp_val['access_token'],
            refresh_token=tgeneration_resp_val['refresh_token'])
        tokens.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        zoho_form_token_generation()
