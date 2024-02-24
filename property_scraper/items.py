# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class PropertyScraperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = Field()
    title = Field()
    type = Field()
    address = Field()
    price = Field()
    description = Field()
    amenities = Field()
    details = Field()
    agent = Field()
    agency_group = Field()
    agency_link = Field()

