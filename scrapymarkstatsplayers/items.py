# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapymarkstatsItem(scrapy.Item):
    # define the fields for your item here like:
    player = scrapy.Field()
    team = scrapy.Field()
    league = scrapy.Field()
    xthreat = scrapy.Field()
    noncrossxt = scrapy.Field()
    fieldsgainedpass = scrapy.Field()
    fieldsgainedcarry = scrapy.Field()
    penboxcarries = scrapy.Field()
    progressionreceived = scrapy.Field()

   




