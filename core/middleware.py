import logging
from django.http import HttpResponseServerError
from django.http import HttpRequest
from django.utils.translation import gettext as _
from django.utils.functional import cached_property

from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from geoip2.errors import GeoIP2Error

from utils.telegram import report_to_admin


class CountryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.country = CountryDetails(request)
        return self.get_response(request)


class CountryDetails:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def _get_country_dict(self):
        # By default, I return where I am located :)
        loc = {"country_code": "DE", "country_name": "Germany"}

        # get IP
        x_forwarded_for = self.request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")

        reporting_active = not ip in ["95.90.192.11", "127.0.0.1"]

        if reporting_active:
            to_admin = f"Path: {self.request.path}\n"
            to_admin += f"IP: {ip}\n"

        g = GeoIP2()

        try:
            loc = g.country(ip)
        except (KeyError, AddressNotFoundError, GeoIP2Error, Exception) as e:
            if reporting_active:
                to_admin += f"🔴 Error getting country: {str(e)}\n"

        if reporting_active:
            to_admin += f"Country: {loc}"
            report_to_admin(to_admin)

        return loc

    @cached_property
    def code(self) -> str:
        return self._get_country_dict()["country_code"]

    @cached_property
    def name(self) -> str:
        return self._get_country_dict()["country_name"]

    def __str__(self):
        return self.code
