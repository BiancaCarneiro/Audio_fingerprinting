# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class musicInfo(scrapy.Item):
    Nome = scrapy.Field()
    Album = scrapy.Field()
    Data = scrapy.Field()
    Artista = scrapy.Field()
    Genero = scrapy.Field()

class GetInfoToDatabaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
