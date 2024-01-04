from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from geoip2.errors import GeoIP2Error

from utils.telegram import report_to_admin


def get_country(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    to_admin = f"IP: {ip}, "

    g = GeoIP2()

    try:
        loc = g.country(ip)
        to_admin += f"Country: {loc}"
        report_to_admin(to_admin)  # TODO: remove
        return loc
    except (KeyError, AddressNotFoundError, Exception):
        # By default, I return where I am located :)
        return {"country_code": "DE", "country_name": "Germany"}
