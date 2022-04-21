"""
Author: Edwin S. Cowart
Created: 4/17/22
"""
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from homeinfo.services.api_view_decorators import (
    api_view_requires_query_param,
    api_view_except_all,
)
from homeinfo.services.house_canary import get_property_details


class HomeViewSet(GenericViewSet, APIView):
    authentication_classes = []
    permission_classes = []

    @api_view_except_all()
    @api_view_requires_query_param("address", "zipcode")
    @action(methods=["get"], detail=False)
    def septic(self, request: Request, *args, **kwargs) -> Response:
        # TODO Next Steps - Validate inbound data, so we don't waste resources or $$$ with a call to an external service
        property_details, exception = get_property_details(
            address=request.query_params["address"],
            zipcode=request.query_params["zipcode"],
        )
        if property_details:
            return Response(property_details.is_septic)
        elif exception:
            message = (
                "Oops! something went wrong with our home info service. "
                f"Please contact us for assistance at {settings.SUPPORT_PHONE_NUMBER}!"
            )
            return Response(
                message,
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        else:
            ValueError(
                "get_property_details must return either a PropertyDetails or an RequestException"
            )
