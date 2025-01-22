import random
import time
import uuid

import scrapy
import wget

from scraper.items import PropertyScraperItem

# 1170 - 1389
# scrapy crawl properties -o properties.csv
# scrapy crawl properties -s SQLITE_LOCATION=properties_data.db


def gen_rand_no():
    used_numbers_lst = []
    for counter in range(5000):
        rand = random.randint(6000, 10000)
        if rand not in used_numbers_lst:
            return rand
        used_numbers_lst.append(rand)


class PropertiesSpider(scrapy.Spider):
    name = "properties"
    allowed_domains = ["www.myproperty.ph"]
    start_urls = [
        "https://www.myproperty.ph/apartment/buy/",
        # "https://www.myproperty.ph/apartment/rent/",
        # "https://www.myproperty.ph/condominium/buy/",
        # "https://www.myproperty.ph/condominium/rent/",
        # "https://www.myproperty.ph/commercial/buy/",
        # "https://www.myproperty.ph/commercial/rent/",
        # "https://www.myproperty.ph/house/buy/",
        # "https://www.myproperty.ph/house/rent/",
        # "https://www.myproperty.ph/land/buy/",
        # "https://www.myproperty.ph/land/rent/",
    ]
    item = PropertyScraperItem()

    def parse(self, response):
        yield response.follow(
            "https://www.myproperty.ph/oxford-suites-residential-studio-unit-for-lease-at-169491572590.html",
            callback=self.parse_leading_link,
        )

        # pages = response.xpath('//div[@class="BaseSection Pagination"]/@data-pagination-end').get()
        # if int(pages) > 1:
        #     listing_page_urls = []
        #     for page in range(1, 3):
        #         next_page_url = f"{response.url}?page={page}"
        #         listing_page_urls.append(next_page_url)
        #         # yield scrapy.Request(next_page_url, callback=self.parse(response=response))
        #     for each_listing in listing_page_urls:
        #         metadata = self.get_metadata(start_url=response.url)
        #         yield response.follow(each_listing, callback=self.parse_listing_url, meta=metadata)
        # else:
        #     metadata = self.get_metadata(start_url=response.url)
        #     yield response.follow(response.url, callback=self.parse_listing_url, meta=metadata)

    def get_metadata(self, start_url):
        metadata = None
        if "/apartment/buy" in start_url:
            metadata = {"type": "apartment", "offer": "buy"}
        elif "/apartment/rent" in start_url:
            metadata = {"type": "apartment", "offer": "rent"}
        elif "/commercial/buy" in start_url:
            metadata = {"type": "commercial", "offer": "buy"}
        elif "/commercial/rent" in start_url:
            metadata = {"type": "commercial", "offer": "rent"}
        elif "/land/buy" in start_url:
            metadata = {"type": "land", "offer": "buy"}
        elif "/land/rent" in start_url:
            metadata = {"type": "land", "offer": "rent"}
        elif "/house/buy" in start_url:
            metadata = {"type": "house", "offer": "buy"}
        elif "/house/rent" in start_url:
            metadata = {"type": "house", "offer": "rent"}
        elif "/condominium/buy" in start_url:
            metadata = {"type": "condominium", "offer": "buy"}
        elif "/condominium/rent" in start_url:
            metadata = {"type": "condominium", "offer": "rent"}

        return metadata

    def parse_listing_url(self, response):
        metadata = response.meta
        property_urls = response.xpath('//a[@class="js-listing-link"]/@href').getall()
        property_urls = list(dict.fromkeys(property_urls))

        for each_url in property_urls:
            yield response.follow(each_url, callback=self.parse_leading_link, meta=metadata)

    def parse_leading_link(self, response):
        self.item["spider"] = self.name
        self.item["property_url"] = response.url
        self.item["type"] = response.meta.get("type")
        self.item["offer"] = response.meta.get("offer")
        self.item["title"] = self.get_property_title(response=response)
        self.item["address"] = self.get_property_address(response=response)
        self.item["price"] = self.get_property_price(response=response)
        self.item["description"] = self.get_property_description(response=response)
        self.item["details"] = self.get_property_details(response=response)
        self.item["amenities"] = self.get_property_amenities(response=response)
        self.item["agent"] = self.get_property_agent(response=response)
        # self.item["agency_group"] = self.get_agency_group(response=response)
        self.item["agent_profile"] = self.get_agency_link(response=response)

        yield self.item

    def get_property_title(self, response):
        property_title = response.xpath("//title/text()").get()
        return str(property_title).strip("\n").strip()

    def get_property_price(self, response):
        price = response.xpath('//div[@class="Title-pdp-price"]//span/text()').get(default="Contact agent for price")
        return price

    def get_property_address(self, response):
        # property address
        extracted_address_string = response.xpath(
            '//div[@id="highlightBox"]//div[@class="HighlightBox_addressLine__BU_xB HighlightBox_highlightItem__1cx9T HighlightBox_secondRow__hV8VU"]/text()'
        ).getall()
        combined_string = "".join(extracted_address_string)
        cleaned_string = " ".join(combined_string.split())
        return cleaned_string

    def get_property_description(self, response):
        prop_li = []
        property_info = response.xpath('//div[@class="ViewMore-text-description"]/p/text()').getall()
        if not property_info:
            property_info = response.xpath('//div[@class="ViewMore-text-description"]/text()').getall()
            for each_p in property_info:
                prop_li.append(each_p.strip().replace("\n", " "))
            return str("".join(prop_li))
        elif not property_info:
            property_info = response.xpath('//div[@class="ViewMore-text-description"]//ul/li/text()').getall()
            for each_p in property_info:
                prop_li.append(each_p.strip().replace("\n", " "))
            return str("".join(prop_li))
        else:
            for each_p in property_info:
                prop_li.append(each_p.strip().replace("\n", " "))
            return str("".join(prop_li))

    def get_property_amenities(self, response):
        try:
            amenities_list = []
            for am in response.xpath(
                '//section[@id="listing-amenities"]//span[@class="listing-amenities-name"]/text()'
            ).getall():
                amenities_list.append(am.strip())

            return str(",".join(amenities_list))
        except:
            return None

    def get_property_agent(self, response):
        try:
            property_agent = response.xpath('//div[@class="AgentInfoV2-agent-name"]/text()').get()
            return str(property_agent).strip().replace("\n", " ")
        except:
            return None

    def get_agency_group(self, response):
        try:
            agency_group = response.xpath('//div[@class="AgentInfoV2-agent-agency"]/a/text()').get()
            return str(agency_group).strip("\n").strip()
        except:
            return None

    def get_agency_link(self, response):
        try:
            agency_link = response.xpath('//div[@class="AgentInfoV2-agent-agency"]/a/@href').get()
            return agency_link
        except:
            return None

    def get_property_details(self, response):
        dict_names = []
        dict_items = []

        try:
            # dict keys
            details_name = response.xpath('//section[@id="listing-details"]//div[@class="ellipsis"]/text()').getall()
            for each_name in details_name:
                if each_name == "":
                    pass
                dict_names.append(each_name.strip())
            for each_name in dict_names:
                dict_names.remove("")

            # dict values
            details_item = response.xpath('//section[@id="listing-details"]//div[@class="last"]/text()').getall()
            for each_item in details_item:
                if each_item == "":
                    pass
                dict_items.append(each_item.strip())

            # full-dict
            full_dict = {dict_names[i]: dict_items[i] for i in range(len(dict_names))}

            if not full_dict:
                return None
            else:
                return full_dict
        except:
            return None

    def get_property_images(self, response):
        img_url = []
        for img_src in response.xpath('//img[@class="swiper-lazy"]/@data-src').getall():
            random_number = gen_rand_no()
            id_ = uuid.uuid4()
            img_name = "{}-{}.jpg".format(id_, random_number)
            img_location = "./images/{}".format(img_name)
            wget.download(img_src, img_location)
            location_to_append = "\images\{}".format(img_name)
            img_url.append(location_to_append)

        return img_url
