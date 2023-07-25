# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import  sqlite3
from scrapytiles.spiders.transferspider import TransferENGSpider,TransferESPSpider,TransferITASpider,TransferGERSpider,TransferFRASpider

class ScrapytilesPipeline:
    def open_spider(self,spider):
        self.con = sqlite3.connect('fbref.db')
        self.cur = self.con.cursor()
        if spider.name==TransferESPSpider.name:
          self.createtable()




    def createtable(self):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS rawtransferstats(  leaguernk integer,league varchar(10),position varchar(10),
        avg_age integer, value integer, avg_value integer )""")
        self.cur.execute("DELETE FROM rawtransferstats")
        self.con.commit()

    def process_item(self, item, spider):
        rows = item['row'].split("!")
        for x in range(len(rows)):
            rows[x]=rows[x].replace('€','')
            rows[x]=rows[x].replace('m', '')
            if rows[x] != '' and rows[x][-1] == 'n':
                rows[x]=round(float(rows[x].replace('bn','')) * 1000, 2)

            elif rows[x][0] != 'A' and rows[x][-1] == 'k':

                rows[x]=round(float(rows[x].replace('k','')) / 1000, 2)

        i=1 if rows[0]!='Total:' else 0
        self.cur.execute('insert into rawtransferstats values( :1, :2, :3, :4,:5,:6)', (item['pos'],item['comp'],
        rows[i], rows[i+1], rows[i+2], rows[i+3]))#to avoid inserting codes other than position
        self.con.commit()
        return item
