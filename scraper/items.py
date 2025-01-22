# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import socket
from datetime import datetime

from scrapy import Field, Item
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class PropertyScraperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    type = Field()
    offer = Field()
    address = Field()
    price = Field()
    description = Field()
    amenities = Field()
    details = Field()
    property_url = Field()
    agent = Field()
    agent_profile = Field()

    # image fields
    image_urls = Field(type=list, default=[])
    images = Field(type=list, default=[])

    # Housekeeping fields
    url = Field(type=str, required=True)
    project = Field(type=str, required=True)
    spider = Field(type=str, required=True)
    server = Field(type=str, required=True)
    extraction_date = Field(type=datetime, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default value for all fields
        for field_name in self.fields:
            if field_name in ["image_urls", "images"]:
                self.setdefault(field_name, [])
            elif field_name == "project":
                self.setdefault(field_name, settings.get("BOT_NAME"))
            elif field_name == "server":
                self.setdefault(field_name, socket.gethostname())
            elif field_name == "extraction_date":
                self.setdefault(field_name, datetime.now().isoformat())
            else:
                self.setdefault(field_name, "")
