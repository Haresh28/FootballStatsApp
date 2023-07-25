# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapymarkstatsItem(scrapy.Item):
    # define the fields for your item here like:
    team = scrapy.Field()
    league=scrapy.Field()
    possesioninper = scrapy.Field()
    fieldtilt = scrapy.Field()
    xt = scrapy.Field()
    xta = scrapy.Field()
    xtdiff = scrapy.Field()
    xg = scrapy.Field()
    xga = scrapy.Field()
    xgdiff = scrapy.Field()
    defline = scrapy.Field()
    oppnbuildinper = scrapy.Field()
    gkprog = scrapy.Field()
    directness = scrapy.Field()




