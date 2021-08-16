# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Petpros1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    StoreName = scrapy.Field()
    Street = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    StoreTiminings = scrapy.Field()
    Phone = scrapy.Field()
    EmailId = scrapy.Field()
    ZipCode = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()

