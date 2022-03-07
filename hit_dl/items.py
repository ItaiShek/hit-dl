import scrapy


class MoodleItem(scrapy.Item):
    path = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()




