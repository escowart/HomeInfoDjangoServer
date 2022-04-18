"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from typing import Tuple, Optional, TypedDict, Literal, Union

from django.conf import settings
from requests import Response, request
from requests.exceptions import RequestException

from homeinfo.requests import HTTPMethod, NonDBModel


def _make_house_canary_api_request(
    method: HTTPMethod, route: str, params: Optional[dict]
) -> Tuple[Response, Optional[RequestException]]:
    """
    :param method: HTTP method
    :param route: House Canary route
    :param params: Query params
    :return: Success: (Response, None)
             Error:   (Response, Exception)
    """
    try:
        response = request(
            method=method,
            url=f"{settings.HOUSE_CANARY_API_URL}/{route}",
            params=params,
            timeout=settings.HOUSE_CANARY_TIMEOUT_S,
        )
        response.raise_for_status()
        return response, None
    except RequestException as e:
        return e.response, e


# NOTE API doc is inconsistent about capitalization. Be sure to casefold when doing comparisons.
Sewer = Literal["Municipal", "None", "Storm", "Septic", "Yes"]


class PropertyDetails(NonDBModel):
    sewer: Sewer

    @property
    def is_septic(self) -> bool:
        return self.sewer.casefold() == "Septic".casefold()


def get_property_details(
    address: str,
) -> Union[Tuple[PropertyDetails, None], Tuple[None, RequestException]]:
    """Get property details
    :param address: Address as a single line string
    :return: Success: (Response, Property, None)
             Error:   (Response, None, Exception)
    """
    # https://api-docs.housecanary.com/#property-details
    response, exception = _make_house_canary_api_request(
        method="get", route="property/details", params={"address": address}
    )
    if exception:
        return None, exception

    property_details_data = response.json()["property/details"]["result"]["property"]
    return PropertyDetails(**property_details_data), None
