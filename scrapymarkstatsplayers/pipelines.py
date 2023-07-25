# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import  sqlite3
class ScrapymarkstatsPipeline:
    def open_spider(self,spider):
        self.con = sqlite3.connect('fbref.db')
        self.cur = self.con.cursor()
        self.createtable()
        print("pep")

    def createtable(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS markstatsplayers(  player varchar(38),playersanaccent varchar(38),squad varchar(38),country varchar(20), xthreat decimal(5,2),noncrossxt decimal(5,2),fieldsgainedpass decimal(5,2),fieldsgainedcarry decimal(5,2),penboxcarries decimal(5,2),progrec decimal(5,2))""")
        self.cur.execute("DELETE FROM markstatsplayers")
        self.con.commit()

    def process_item(self, item, spider):
        self.cur.execute('insert into markstatsplayers values( :1, :2, :3, :4,:5,:6,:7,:8,:9,:10)', (item['player'],
        item['player'], item["team"], item["league"], item["xthreat"], item["noncrossxt"], item["fieldsgainedpass"],
        item["fieldsgainedcarry"], item["penboxcarries"], item["progressionreceived"]))
        self.con.commit()
        return item

