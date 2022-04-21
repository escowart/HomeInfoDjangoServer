"""
Author: Edwin S. Cowart
Created: 4/18/22
"""
import logging
from unittest.mock import patch
from django.test import TestCase, Client

from homeinfo.services.house_canary import get_property_details


class HomeSewerTestCase(TestCase):
    def setUp(self):
        """Run administrative tasks."""
        self.client = Client()

    @patch("homeinfo.services.house_canary.requests.get")
    def test_home_sewer_success(self, mock_request):
        # TODO - Next Step - Find a better way to parameterize a test
        cases = (
            ("Septic", True),
            ("septic", True),
            ("Municipal", False),
            ("municipal", False),
        )
        for sewer, is_septic in cases:
            self._test_home_sewer_success(mock_request, sewer, is_septic)

    def _test_home_sewer_success(
        self, mock_request, sewer: str, is_septic: bool
    ):
        # Define response data for my Mock object
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "property/details": {
                "api_code_description": "ok",
                "api_code": 0,
                "result": {
                    "property": {
                        "air_conditioning": "yes",
                        "attic": False,
                        "basement": "full_basement",
                        "building_area_sq_ft": 1824,
                        "building_condition_score": 5,
                        "building_quality_score": 3,
                        "construction_type": "Wood",
                        "exterior_walls": "wood_siding",
                        "fireplace": False,
                        "full_bath_count": 2,
                        "garage_parking_of_cars": 1,
                        "garage_type_parking": "underground_basement",
                        "heating": "forced_air_unit",
                        "heating_fuel_type": "gas",
                        "no_of_buildings": 1,
                        "no_of_stories": 2,
                        "number_of_bedrooms": 4,
                        "number_of_units": 1,
                        "partial_bath_count": 1,
                        "pool": True,
                        "property_type": "Single Family Residential",
                        "roof_cover": "Asphalt",
                        "roof_type": "Wood truss",
                        "site_area_acres": 0.119,
                        "style": "colonial",
                        "total_bath_count": 2.5,
                        "total_number_of_rooms": 7,
                        "sewer": sewer,
                        "subdivision": "CITY LAND ASSOCIATION",
                        "water": "municipal",
                        "year_built": 1957,
                        "zoning": "RH1",
                    },
                    "assessment": {
                        "apn": "0000 -1111",
                        "assessment_year": 2015,
                        "tax_year": 2015,
                        "total_assessed_value": 1300000.0,
                        "tax_amount": 15199.86,
                    },
                },
            }
        }

        # Call the function
        property_details, exception = get_property_details(
            address="123+Main+St", zipcode="20500"
        )
        self.assertIsNotNone(property_details)
        self.assertEqual(property_details.sewer, sewer)
        self.assertEqual(property_details.is_septic, is_septic)
        self.assertIsNone(exception)

        response = self.client.get(
            f"/home/septic", {"address": "123+Main+St", "zipcode": "20500"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), is_septic)

    def test_home_sewer_test_live_url(self):
        # Test live URL which will return a 401 Client Error: UNAUTHORIZED
        logging.disable()
        property_details, exception = get_property_details(
            address="123+Main+St", zipcode="20500"
        )
        self.assertIsNone(property_details)
        self.assertIsNotNone(exception)
        response = exception.response
        self.assertEqual(response.status_code, 401)
        message = (
            "The request does not contain required authentication parameters. "
            "Please use one of the authentication protocols supported by "
            "HouseCanary APIs."
        )
        self.assertEqual(response.json(), {"message": message})
        response = self.client.get(
            f"/home/septic", {"address": "123+Main+St", "zipcode": "20500"}, follow=True
        )
        logging.disable(False)
        message = (
            "Oops! something went wrong with our home info service. "
            "Please contact us for assistance at 1-800-123-5678!"
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), message)

    def test_home_bad_request(self):
        # TODO - Next Step - Find a better way to parameterize a test
        cases = (
            ({}, "Missing require query params: address and zipcode"),
            (
                {
                    "address": "123+Main+St",
                },
                "Missing require query param: zipcode",
            ),
            ({"zipcode": "20500"}, "Missing require query param: address"),
        )
        for query_params, expected_json_response in cases:
            self._test_home_bad_request(query_params, expected_json_response)

    def _test_home_bad_request(self, query_params: dict, expected_json_response: str):
        response = self.client.get(f"/home/septic", query_params, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_json_response)

    @patch("homeinfo.services.house_canary.requests.get")
    def test_contract_violation_from_service(self, mock_request):
        cases = (
            "Contract Violation",
            {"another-one": "another-one"},
            {
                "property/details": {"result": "Contract Violation"}
            },
            {
                "property/details": {"result": {
                    "sewer": 123
                }}
            }
        )
        for case in cases:
            self._test_contract_violation_from_service(mock_request, case)

    def _test_contract_violation_from_service(self, mock_request, response_json_property_details: dict):
        # Define response data for my Mock object
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "property/details": response_json_property_details
        }
        # TODO - Next Steps - Investigate how to disable logging if a test succeeds
        logging.disable()
        response = self.client.get(
            f"/home/septic", {"address": "123+Main+St", "zipcode": "20500"}, follow=True
        )
        logging.disable(False)
        message = (
            "Oops! something went wrong with our home info service. "
            "Please contact us for assistance at 1-800-123-5678!"
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), message)
