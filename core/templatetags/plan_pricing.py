from decimal import Decimal

from django import template
from django.conf import settings
from django.db.models import Max, Min, Avg


from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money

from ..models.countries import Country

register = template.Library()


def round0_005(d: Decimal):
    return round(Decimal(0.005 * round(1000 * d / 5)), 3)


@register.simple_tag
def get_plan_price(request, plan) -> Money:
    """Get price depending on the GDP per capita"""
    countries = Country.objects.all()
    gdp_min = countries.aggregate(Min("gdp"))["gdp__min"]
    gdp_max = countries.aggregate(Max("gdp"))["gdp__max"]
    gdp_avg = countries.aggregate(Avg("gdp"))["gdp__avg"]
    p_min = plan.price_min.amount
    p_max = plan.price_max.amount
    in_currency = str(plan.price_min.currency)

    # Get the GDP and the desired currency
    try:
        country = countries.filter(code=request.country.code)[0]
        gdp, out_currency = country.gdp, country.currency
    except (IndexError, AttributeError):
        gdp, out_currency = gdp_avg, in_currency

    # Calculate the price (interpolation)
    price_amount = p_min + (gdp - gdp_min) / (gdp_max - gdp_min) * (p_max - p_min)
    in_money = Money(price_amount, in_currency)

    # Convert
    out_money = convert_money(in_money, out_currency)

    if out_currency in settings.THREE_DECIMAL_CURRENCIES:
        return Money(round0_005(out_money.amount), out_currency)
    elif out_currency in settings.ZERO_DECIMAL_CURRENCIES:
        return Money(round(out_money.amount, 0), out_currency)
    elif out_currency in settings.STANDARD_CURRENCIES:
        return out_money
    else:
        return in_money


def get_currency_and_amount_for_stripe(request, plan) -> (str, int):
    money = get_plan_price(request, plan)
    curr = str(money.currency)
    amount = int(100 * money.amount)
    if curr in settings.THREE_DECIMAL_CURRENCIES:
        amount = int(1000 * money.amount)
    if curr in settings.ZERO_DECIMAL_CURRENCIES:
        amount = int(money.amount)

    return curr.lower(), amount
