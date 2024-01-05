from django.conf import settings
from django.http import HttpRequest
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
        # get IP
        x_forwarded_for = self.request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")

        g = GeoIP2()

        try:
            country_dict = g.country(ip)
        except Exception as e:
            # If there is an Exception, return where I am located :)
            country_dict = {"country_code": "DE", "country_name": "Germany"}
            if not settings.DEBUG:
                report_to_admin(f"🔴 Error getting country for {ip}:\n\n{str(e)}")

        return country_dict

    @cached_property
    def code(self) -> str:
        return self._get_country_dict()["country_code"]

    @cached_property
    def name(self) -> str:
        return self._get_country_dict()["country_name"]

    def __str__(self):
        return self.code
