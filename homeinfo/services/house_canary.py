"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
import logging
import requests  # Import has to be structured this way for unittest.mock.patch
from typing import Tuple, Optional, Literal, Union, TypeVar
from django.conf import settings

HTTPMethod = Literal["get", "options", "head", "post", "put", "patch", "delete"]

T = TypeVar('T')


def _get_property_attribute_from_house_canary_api(
        attribute: str, params: Optional[dict]
) -> Union[Tuple[T, None], Tuple[None, Exception]]:
    """
    Get property attribute from the House Canary API
    :param attribute: property attribute
    :param params: Query params
    :return: Success: (Response, None)
             Error:   (None, Exception)
    """
    try:
        response = requests.get(
            url=f"{settings.HOUSE_CANARY_API_URL}/property/{attribute}",
            params=params,
            timeout=settings.HOUSE_CANARY_TIMEOUT_S,
        )
        response.raise_for_status()
        # https://api-docs.housecanary.com/#property-census
        # If you view the House Canaray API documentation, you'll see that requests to fetch property attributes
        # have a standard response structure
        result = response.json()[f"property/{attribute}"]["result"]
        return result, None
    except (requests.exceptions.RequestException, TypeError, KeyError) as e:
        # TODO Next Step log exception to exception monitoring service
        logging.exception(e, stack_info=True)
        # RequestException when:
        #   - Timeout
        #   - Connection/Session issue
        #   - Response isn't JSON
        #   - Response is 400/500-series
        # ValueError when:
        #   - Response JSON is missing a key
        return None, e


# NOTE API doc is inconsistent about capitalization. Be sure to casefold when doing comparisons.
# TODO Next Step - Investigate converting str -> Enum & Enum validation
Sewer = Literal["Municipal", "None", "Storm", "Septic", "Yes"]


class PropertyDetails:
    # Other attributes are omitted because they are unused
    sewer: Sewer

    # TODO Next Step - Create a non-DB object deserializer
    def __init__(self, **kwargs):
        self.sewer = kwargs.get("sewer")
        self._validate()

    def _validate(self):
        if not isinstance(self.sewer, str):
            raise TypeError("Sewer must be a string")
        # TODO Next Step - Validate the sewer value is part of the expected enum

    @property
    def is_septic(self) -> bool:
        return self.sewer.casefold() == "Septic".casefold()


def get_property_details(
    address: str, zipcode: str
) -> Union[Tuple[PropertyDetails, None], Tuple[None, Exception]]:
    """Get property details
    :param address: Single line address
    :param zipcode: Zip code
    :return: Success: (Response, Property, None)
             Error:   (Response, None, Exception)
    """
    # https://api-docs.housecanary.com/#property-details
    result, exception = _get_property_attribute_from_house_canary_api(
        attribute="details",
        params={"address": address, "zipcode": zipcode},
    )
    if exception:
        return None, exception

    try:
        property_details = PropertyDetails(**result["property"])
        return property_details, None
    except (TypeError, KeyError) as e:
        return None, e
