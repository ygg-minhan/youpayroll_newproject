import logging
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def tgeneration_call_api(url, data):
    """ Generate tokens"""
    response = None
    try:
        response = requests.post(url=url, data=data, timeout=30)
        logger.info("Token generation is successful")
        response.raise_for_status()
    except HTTPError as errh:
        logger.warning(f"Http Error:{errh}")
    except ConnectionError as errc:
        logger.warning(f"Error Connecting:{errc}")
    except Timeout as errt:
        logger.warning(f"Timeout Error:{errt}")
    except RequestException as err:
        logger.warning(f"OOps: Something Else:{err}")

    return response
