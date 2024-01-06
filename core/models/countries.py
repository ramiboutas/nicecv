from decimal import Decimal


import requests
from bs4 import BeautifulSoup

from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=8, unique=True, db_index=True)
    name = models.CharField(max_length=64)
    gdp = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal(50_000))
    currency = models.CharField(max_length=8)
    wikipedia_url = models.URLField(max_length=128)

    def __str__(self):
        return self.code + " " + self.name

    @classmethod
    def scrap_from_wikipedia(cls):
        if cls.objects.count() > 0:
            print("## Info: Not possible to scrap, since there the objects in the db")
            return

        host = "https://en.wikipedia.org"
        url = host + "/wiki/List_of_countries_by_GDP_(nominal)_per_capita"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class": "wikitable"})
        for row in table.tbody.find_all("tr"):
            name, gdp, c_url = None, None, None
            columns = row.find_all("td")
            if columns != []:
                name = columns[0].text.strip()
                c_url = host + columns[0].find_next("a").get("href")
                gdp = columns[2].text.strip().replace(",", "")
                c_r = requests.get(c_url)
                c_soup = BeautifulSoup(c_r.text, "html.parser")
                c_table = c_soup.find("table", {"class": "vcard"})
                print(c_url)
                currency, code = None, None
                for c_tr in c_table.tbody.find_all("tr"):
                    for c_child in c_tr.children:
                        if c_child.name == "th":
                            td = c_child.next_sibling
                            if c_child.text == "Currency":
                                try:
                                    anchors = td.find_all("a")
                                    currency = [
                                        a
                                        for a in anchors
                                        if "ISO 4217" in a.get("title")
                                    ][0].text
                                except Exception as e:
                                    print(e)

                            if "ISO 3166" in c_child.text:
                                code = td.find_all("a")[0].text
                properties = (name, gdp, c_url, currency, code)
                if all(properties):
                    cls.objects.create(
                        name=name,
                        code=code,
                        currency=currency,
                        wikipedia_url=c_url,
                        gdp=gdp,
                    )
                else:
                    print(f"## Error {properties} ")
