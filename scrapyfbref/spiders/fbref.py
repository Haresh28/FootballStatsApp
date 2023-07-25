import scrapy
from ..items import ScrapyfbrefItem
from scrapy.loader import ItemLoader
#from scrapyfbref.items import ScrapyfbrefItem #for shell running

class FbrefSpider(scrapy.Spider):
    name = 'fbrefleague'
    allowed_domains = ['fbref.com']
    start_urls = ["https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats"]

    def parse(self, response):

        for rows in response.css('table.min_width').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)
                    l.add_css('row','th')
                    l.add_css('row','td')

                    #item['row']=[rows.css('th.right::text').getall(),rows.css('td::text')]
                    yield l.load_item()


                    #'row':rows.css('th::text').getall()
class FbrefSCASpider(scrapy.Spider):
    name = 'fbrefSCA'
    allowed_domains = ['fbref.com']
    start_urls = ["https://fbref.com/en/comps/Big5/gca/squads/Big-5-European-Leagues-Stats"]

    def parse(self, response):

        for rows in response.css('table.min_width').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)
                    l.add_css('row','th')
                    l.add_css('row','td')

                    #item['row']=[rows.css('th.right::text').getall(),rows.css('td::text')]
                    yield l.load_item()


class FbrefGCASpider(scrapy.Spider):
    name = 'fbrefgca'
    allowed_domains = ['fbref.com']
    start_urls = ["https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats"]

    def parse(self, response):

        for rows in response.css('table.min_width').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)
                    l.add_css('row','th')
                    l.add_css('row','td')

                    #item['row']=[rows.css('th.right::text').getall(),rows.css('td::text')]
                    yield l.load_item()


class FbrefAGKSpider(scrapy.Spider):
    name = 'fbrefagk'
    allowed_domains = ['fbref.com']
    start_urls = ["https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats"]

    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()


class FbrefGKSpider(scrapy.Spider):
    name = 'fbrefgk'
    allowed_domains = ['fbref.com']
    start_urls = ["https://fbref.com/en/comps/Big5/keepers/players/Big-5-European-Leagues-Stats"]

    def parse(self, response):
        for rows in response.css('table.stats_table').css('tr'):
            l = ItemLoader(item=ScrapyfbrefItem(), selector=rows)

            l.add_css('row', 'th')
            l.add_css('row', 'td')
            yield l.load_item()


class FbrefDEFSpider(scrapy.Spider):
    name = 'fbrefdef'
    allowed_domains = ['fbref.com']
    start_urls = ["https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats"]

    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()


class FbrefSTDSpider(scrapy.Spider):
    name = 'fbrefstd'
    allowed_domains = ['fbref.com']
    start_urls = ['https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats']


    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()

class FbrefSHTSpider(scrapy.Spider):
    name = 'fbrefsht'
    allowed_domains = ['fbref.com']
    start_urls = ['https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats']


    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()

class FbrefPASSpider(scrapy.Spider):
    name = 'fbrefpas'
    allowed_domains = ['fbref.com']
    start_urls = ['https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats']


    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()
class FbrefPSTSpider(scrapy.Spider):
    name = 'fbrefpst'
    allowed_domains = ['fbref.com']
    start_urls = ['https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats']


    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()


class FbrefPOSSpider(scrapy.Spider):
    name = 'fbrefpos'
    allowed_domains = ['fbref.com']
    start_urls = ['https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats']


    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()


class FbrefMISSpider(scrapy.Spider):
    name = 'fbrefmis'
    allowed_domains = ['fbref.com']
    start_urls = ['https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats']


    def parse(self, response):

        for rows in response.css('table.stats_table').css('tr'):
                    l = ItemLoader(item=ScrapyfbrefItem(),selector=rows)

                    l.add_css('row','th')
                    l.add_css('row','td')
                    yield l.load_item()


#all spiders generate some unnecessary data
#except gk stats all others can be matched with their rank as playerid
