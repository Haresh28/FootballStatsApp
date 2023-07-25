# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, SelectJmes,Join,Compose,Identity
from w3lib.html import remove_tags


class ScrapytilesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    row= scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = Join('!'))
    pos=scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = Join('!'))
    comp = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join('!'))

