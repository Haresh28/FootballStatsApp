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

        self.cur.execute("""CREATE TABLE IF NOT EXISTS markstats(  squad varchar(38),country varchar(20), possesion decimal(5,2),fieldtilt decimal(5,2),xt decimal(5,2),xta decimal(5,2),xtdiff decimal(5,2),
        xg decimal(5,2), xga decimal(5,2), xgdiff decimal(5,2) ,defline decimal(5,2),oppnbuidup decimal(5,2),gkprogression decimal(5,2),directness decimal(5,2))""")
        self.cur.execute("DELETE FROM markstats")
        self.con.commit()

    def process_item(self, item, spider):

        self.cur.execute('insert into markstats values( :1, :2, :3, :4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)', (item["team"] ,item["league"],item["possesioninper"],item["fieldtilt"],item["xt"],item["xta"],item["xtdiff"], item["xg"],item["xga"],item["xgdiff"],item["defline" ],item["oppnbuildinper"],item["gkprog"],item["directness"] ))
        self.con.commit()
        return item

