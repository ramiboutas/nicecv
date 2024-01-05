from decimal import Decimal

from django import template
from django.db.models import Max, Min


from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money

from ..models.countries import Country

register = template.Library()


@register.simple_tag
def get_plan_price(request, plan):
    """Get price depending on the GDP per capita"""
    countries = Country.objects.all()
    p_min = plan.price_min.amount
    p_max = plan.price_max.amount
    gdp_min = countries.aggregate(Min("gdp"))["gdp__min"]
    gdp_max = countries.aggregate(Max("gdp"))["gdp__max"]
    try:
        country = countries.filter(code=request.country.code)[0]
        gdp, out_currency = country.gdp, country.currency
    except (IndexError, AttributeError):
        gdp, out_currency = Decimal(50000), "EUR"

    price_amount = p_min + (gdp - gdp_min) / (gdp_max - gdp_min) * (p_max - p_min)
    in_currency = plan.price_min.currency
    return convert_money(Money(price_amount, in_currency), out_currency)
