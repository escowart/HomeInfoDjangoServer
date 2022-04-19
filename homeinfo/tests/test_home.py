"""
Author: Edwin S. Cowart
Created: 4/18/22
"""
from unittest.mock import patch
from django.test import TestCase

from django.test import Client

from homeinfo.services.housecanary import get_property_details

mock_property_details = {
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
    "sewer": "municipal",
    "subdivision": "CITY LAND ASSOCIATION",
    "water": "municipal",
    "year_built": 1957,
    "zoning": "RH1",
}

mock_assessment = {
    "apn": "0000 -1111",
    "assessment_year": 2015,
    "tax_year": 2015,
    "total_assessed_value": 1300000.0,
    "tax_amount": 15199.86,
}


@patch("homeinfo.services.housecanary.requests.request")
class HomeSewerTestCase(TestCase):
    def setUp(self):
        """Run administrative tasks."""
        self.client = Client()

    def test_home_municipal_sewer_success(self, mock_request):
        # Define response data for my Mock object
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "property/details": {
                "api_code_description": "ok",
                "api_code": 0,
                "result": {
                    "property": mock_property_details,
                    "assessment": mock_assessment,
                },
            }
        }

        # Call the function
        property_details, exception = get_property_details(
            address="123+Main+St", zipcode="20500"
        )
        self.assertEqual(property_details.sewer, "municipal")
        self.assertFalse(property_details.is_septic)

    def test_api(self, mock_request):
        response = self.client.get(
            f"/home/septic", {"address": "123+Main+St", "zipcode": "20500"}
        )
        # Don't have permission to access the API
        self.assertEqual(response.status_code, 503)
