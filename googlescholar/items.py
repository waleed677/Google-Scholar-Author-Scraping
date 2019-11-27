# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy 


class GooglescholarItem(scrapy.Item):
    # define the fields for your item here like:
     name = scrapy.Field()
     email = scrapy.Field()
     tags = scrapy.Field()
     position = scrapy.Field()
     citation = scrapy.Field()
     citation_2014 = scrapy.Field()
     hindex = scrapy.Field()
     hindex_2014 = scrapy.Field()
     iindex = scrapy.Field()
     iindex_2014 = scrapy.Field()
     totaltitle = scrapy.Field()
     maxyear = scrapy.Field()
     minyear = scrapy.Field()
    
