from decimal import Decimal

from django import template
from django.db.models import Max, Min


from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money

from ..models.countries import Country

register = template.Library()
# https://stripe.com/docs/currencies?presentment-currency=DE#presentment-currencies
# Currencies marked with * are not supported by American Express
STANDARD_CURRENCIES = (
    "USD",
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BRL",
    "BSD",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHF",
    "CLP",
    "CNY",
    "COP",
    "CRC",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JMD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KRW",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SOS",
    "SRD",
    "STD",
    "SZL",
    "THB",
    "TJS",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "UYU",
    "UZS",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XCD",
    "XOF",
    "XPF",
    "YER",
    "ZAR",
    "ZMW",
)
# https://stripe.com/docs/currencies?presentment-currency=DE#zero-decimal
ZERO_DECIMAL_CURRENCIES = (
    "BIF",
    "CLP",
    "DJF",
    "GNF",
    "JPY",
    "KMF",
    "KRW",
    "MGA",
    "PYG",
    "RWF",
    "UGX",
    "VND",
    "VUV",
    "XAF",
    "XOF",
    "XPF",
)

# https://stripe.com/docs/currencies?presentment-currency=DE#three-decimal

THREE_DECIMAL_CURRENCIES = ("BHD", "JOD", "KWD", "OMR", "TND")


def round5(x):
    return 5 * round(x / 5)


def get_currency_and_amount(money: Money):
    if money.currency in STANDARD_CURRENCIES:
        return money.currency, int(100 * money.amount)
    elif money.currency in ZERO_DECIMAL_CURRENCIES:
        return money.currency, int(money.amount)
    elif money.currency in THREE_DECIMAL_CURRENCIES:
        return money.currency, round5(int(1000 * money.amount))
    else:
        return ("EUR", int(100 * convert_money(money, "EUR").amount))


@register.simple_tag
def get_plan_price(request, plan):
    """Get price depending on the GDP per capita"""
    countries = Country.objects.all()
    gdp_min = countries.aggregate(Min("gdp"))["gdp__min"]
    gdp_max = countries.aggregate(Max("gdp"))["gdp__max"]
    p_min = plan.price_min.amount
    p_max = plan.price_max.amount
    in_currency = plan.price_min.currency

    # Get the GDP and the desired currency
    try:
        country = countries.filter(code=request.country.code)[0]
        gdp, out_currency = country.gdp, country.currency
    except (IndexError, AttributeError):
        gdp, out_currency = Decimal(50000), in_currency

    price_amount = p_min + (gdp - gdp_min) / (gdp_max - gdp_min) * (p_max - p_min)
    in_money = Money(price_amount, in_currency)
    out_money = convert_money(in_money, out_currency)

    if out_currency in THREE_DECIMAL_CURRENCIES:
        return Money(round5(int(out_money.amount)), out_currency)
    elif out_currency in ZERO_DECIMAL_CURRENCIES:
        return Money(int(out_money.amount), out_currency)
    elif out_currency in STANDARD_CURRENCIES:
        return out_money
    else:
        return in_money


def get_currency_and_amount_for_stripe(request, plan):
    money = get_plan_price(request, plan)
    curr = str(money.currency)
    amount = int(100 * money.amount)
    if curr in ZERO_DECIMAL_CURRENCIES:
        amount = int(money.amount)
    elif curr in THREE_DECIMAL_CURRENCIES:
        amount = int(1000 * money.amount)

    return curr.lower(), amount
