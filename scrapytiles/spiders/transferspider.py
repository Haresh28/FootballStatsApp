import scrapy
from scrapytiles.items import ScrapytilesItem
from scrapy.loader import ItemLoader


class TransferENGSpider(scrapy.Spider):
    name = 'eng ENG'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1']

    def parse(self, response):
        for link in response.css('div.large-8.columns').css('table.items').css('td.hauptlink.no-border-links').css('a'):
            if link.attrib['href']!="#":
                #("verification:   ",'http://www.transfermarkt.com'+link.attrib['href'].replace('startseite', 'kader'))
                try:
                    yield response.follow('http://www.transfermarkt.com'+link.attrib['href'].replace('startseite', 'kader'),callback=self.parse_clubs)
                except:
                    exit(1)

    def parse_clubs(self, response):

        for data in response.css('div.large-4.columns tr'):
            l = ItemLoader(item=ScrapytilesItem(), selector=data)

            # l.add_css('row', 'th')
            l.add_css('row', 'td')
            # data=response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2]

            item = l.load_item()
            if len(item.keys()) != 0:  # to eliminate empty item objects
                item['pos'] = \
                response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2].get()
                item['comp'] = 'eng ENG'
                yield item


class TransferESPSpider(scrapy.Spider):
    name = 'es ESP'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1']

    def parse(self, response):
        for link in response.css('div.large-8.columns').css('table.items').css('td.hauptlink.no-border-links').css('a'):
            if link.attrib['href'] != "#":
                # ("verification:   ",'http://www.transfermarkt.com'+link.attrib['href'].replace('startseite', 'kader'))
                try:
                    yield response.follow(
                        'http://www.transfermarkt.com' + link.attrib['href'].replace('startseite', 'kader'),
                        callback=self.parse_clubs)
                except:
                    exit(1)

    def parse_clubs(self, response):

        for data in response.css('div.large-4.columns tr'):
            l = ItemLoader(item=ScrapytilesItem(), selector=data)

            # l.add_css('row', 'th')
            l.add_css('row', 'td')
            # data=response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2]

            item = l.load_item()
            if len(item.keys()) != 0:  # to eliminate empty item objects
                item['pos'] = \
                response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2].get()
                item['comp'] = 'es ESP'
                yield item


class TransferGERSpider(scrapy.Spider):
    name = 'ger'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1']

    def parse(self, response):
        for link in response.css('div.large-8.columns').css('table.items').css('td.hauptlink.no-border-links').css('a'):
            if link.attrib['href'] != "#":
                # ("verification:   ",'http://www.transfermarkt.com'+link.attrib['href'].replace('startseite', 'kader'))
                try:
                    yield response.follow(
                        'http://www.transfermarkt.com' + link.attrib['href'].replace('startseite', 'kader'),
                        callback=self.parse_clubs)
                except:
                    exit(1)

    def parse_clubs(self, response):

        for data in response.css('div.large-4.columns tr'):
            l = ItemLoader(item=ScrapytilesItem(), selector=data)

            # l.add_css('row', 'th')
            l.add_css('row', 'td')
            # data=response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2]

            item = l.load_item()
            if len(item.keys()) != 0:  # to eliminate empty item objects
                item['pos'] = \
                response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2].get()
                item['comp'] = 'de GER'
                yield item


class TransferITASpider(scrapy.Spider):
    name = 'ita'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1']

    def parse(self, response):
        for link in response.css('div.large-8.columns').css('table.items').css('td.hauptlink.no-border-links').css('a'):
            if link.attrib['href'] != "#":
                # ("verification:   ",'http://www.transfermarkt.com'+link.attrib['href'].replace('startseite', 'kader'))
                try:
                    yield response.follow(
                        'http://www.transfermarkt.com' + link.attrib['href'].replace('startseite', 'kader'),
                        callback=self.parse_clubs)
                except:
                    exit(1)

    def parse_clubs(self, response):

        for data in response.css('div.large-4.columns tr'):
            l = ItemLoader(item=ScrapytilesItem(), selector=data)

            # l.add_css('row', 'th')
            l.add_css('row', 'td')
            # data=response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2]

            item = l.load_item()
            if len(item.keys()) != 0:  # to eliminate empty item objects
                item['pos'] =response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2].get()
                item['comp'] = 'it ITA'
                yield item


class TransferFRASpider(scrapy.Spider):
    name = 'fra'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1']

    def parse(self, response):
        for link in response.css('div.large-8.columns').css('table.items').css('td.hauptlink.no-border-links').css('a'):
            if link.attrib['href'] != "#":
                # ("verification:   ",'http://www.transfermarkt.com'+link.attrib['href'].replace('startseite', 'kader'))
                try:
                    yield response.follow(
                        'http://www.transfermarkt.com' + link.attrib['href'].replace('startseite', 'kader'),
                        callback=self.parse_clubs)
                except:
                    exit(1)

    def parse_clubs(self, response):

        for data in response.css('div.large-4.columns tr'):
            l = ItemLoader(item=ScrapytilesItem(), selector=data)

            #l.add_css('row', 'th')
            l.add_css('row', 'td')
            #data=response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2]

            item=l.load_item()
            if len(item.keys())!=0:#to eliminate empty item objects
                item['pos']=response.css('div.data-header__club-info').css('span.data-header__content').css('a::text')[2].get()
                item['comp']='fr FRA'
                yield item
