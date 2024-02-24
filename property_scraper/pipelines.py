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
            link text,
            title text,
            type text,
            offer text,
            address text,
            price text,
            description text,
            amenities text,
            details text,
            agent text,
            agency_group text,
            agency_link text
        )
        """)
        
    def process_item(self, item, spider):
        ## Check to see if title is already in database 
        self.cur.execute("select * from properties where link = %s", (item['link'],))
        result = self.cur.fetchone()
        
        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            ## Define insert statement
            self.cur.execute(""" 
                insert into properties(
                    link, 
                    title, 
                    type,
                    offer,
                    address, 
                    price,
                    description,
                    amenities,
                    details,
                    agent,
                    agency_group,
                    agency_link
                )values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['link'], item['title'], item['type'], item['offer'], str(item['address']), 
                    str(item['price']), item['description'], str(item['amenities']), str(item['details']),
                    item['agent'], item['agency_group'], item['agency_link']
                )
            )

            ## Execute insert of data into database
            self.connection.commit()
        return item
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
