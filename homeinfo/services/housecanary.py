"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from typing import Tuple, Optional, Literal, Union

from django.conf import settings
import requests  # Import has to be structured this way for the unittest to work

from homeinfo.services.logging import log_exception
from homeinfo.utility import HTTPMethod, NonDBModel


def _make_house_canary_api_request(
    method: HTTPMethod, route: str, params: Optional[dict]
) -> Tuple[requests.Response, Optional[requests.exceptions.RequestException]]:
    """
    :param method: HTTP method
    :param route: House Canary route
    :param params: Query params
    :return: Success: (Response, None)
             Error:   (Response, Exception)
    """
    try:
        response = requests.request(
            method=method,
            url=f"{settings.HOUSE_CANARY_API_URL}/{route}",
            params=params,
            timeout=settings.HOUSE_CANARY_TIMEOUT_S,
        )
        response.raise_for_status()
        return response, None
    except requests.exceptions.RequestException as e:
        return e.response, e


# NOTE API doc is inconsistent about capitalization. Be sure to casefold when doing comparisons.
Sewer = Literal["Municipal", "None", "Storm", "Septic", "Yes"]


class PropertyDetails(NonDBModel):
    sewer: Sewer

    @property
    def is_septic(self) -> bool:
        return self.sewer.casefold() == "Septic".casefold()


def get_property_details(
    address: str, zipcode: str
) -> Union[Tuple[PropertyDetails, None], Tuple[None, requests.RequestException]]:
    """Get property details
    :param address: Single line address
    :param zipcode: Zip code
    :return: Success: (Response, Property, None)
             Error:   (Response, None, Exception)
    """
    # https://api-docs.housecanary.com/#property-details
    response, exception = _make_house_canary_api_request(
        method="get",
        route="property/details",
        params={"address": address, "zipcode": zipcode},
    )
    if exception:
        log_exception(exception)
        return None, exception

    property_details_data = response.json()["property/details"]["result"]["property"]
    return PropertyDetails(**property_details_data), None
