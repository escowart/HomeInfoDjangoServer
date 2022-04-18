"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from homeinfo.decorators import api_view_requires_query_param
from homeinfo.housecanary import get_property_details
from homeinfo.requests import to_rest_framework_response


class HomeViewSet(GenericViewSet, APIView):
    authentication_classes = []
    permission_classes = []

    @api_view_requires_query_param("address")
    @action(methods=["get"], detail=False)
    def septic(self, request: Request, *args, **kwargs) -> Response:
        property_details, exception = get_property_details(
            request.query_params["address"]
        )
        if property_details:
            return Response(property_details.is_septic)
        elif exception:
            return to_rest_framework_response(exception.response)
        else:
            ValueError(
                "get_property_details must return either a PropertyDetails or an RequestException"
            )
