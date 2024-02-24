# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os


class PropertyScraperPipeline:
    
    def __init__(self):
        ## Connection Details
        hostname = os.environ.get('HOSTNAME')
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD') # your password
        database = os.environ.get('DATABASE')

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS properties(
            id serial PRIMARY KEY, 
            link_to_property text,
            property_title text,
            property_type text,
            property_address text,
            property_price text,
            property_description text,
            property_amenities text,
            property_details text,
            property_agent text,
            agency_group text,
            agency_link text
        )
        """)
        
    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" 
            insert into properties(
                link_to_property, 
                property_title, 
                property_type, 
                property_address, 
                property_price,
                property_description,
                property_amenities,
                property_details,
                property_agent,
                agency_group,
                agency_link
            )values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                item['link_to_property'], item['property_title'], item['property_type'],
                str(item['property_address']), str(item['property_price']), item['property_description'],
                str(item['property_amenities']), str(item['property_details']),
                item['property_agent'], item['agency_group'], item['agency_link']
            )
        )

        ## Execute insert of data into database
        self.connection.commit()
        return item
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
