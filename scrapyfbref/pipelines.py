# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
#from spiders.fbref import FbrefSpider,FbrefGKSpider,FbrefDEFSpider,FbrefSTDSpider
from scrapyfbref.spiders.fbref import FbrefSpider,FbrefSCASpider,FbrefGKSpider,FbrefDEFSpider,FbrefSTDSpider,FbrefAGKSpider,FbrefGCASpider,FbrefMISSpider,FbrefPOSSpider,FbrefPSTSpider,FbrefPASSpider,FbrefSHTSpider


class ScrapyfbrefPPipeline:

    def open_spider(self,spider):
        self.con = sqlite3.connect('fbref.db')
        self.cur = self.con.cursor()
        if spider.name==FbrefSTDSpider.name:

            self.createtable()



    def createtable(self):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS lstanding(  squad varchar(38),country varchar(20),leaguernk integer default 0,
        mp integer default 0, won integer default 0, drawn integer default 0, lost integer default 0, gf integer default 0, ga integer default 0, gd integer default 0, pts integer default 0,
        pts_g decimal(5,2) default 0, xg decimal(5,2) default 0, xga decimal(5,2) default 0, xgd decimal(5,2) default 0,xgd_per_match decimal(5,2) default 0,
        attendace integer default 0, top_team_scorer varchar(60) )""")
        self.cur.execute("DELETE FROM lstanding")


        self.cur.execute("""CREATE TABLE IF NOT EXISTS goalshotcreation(  squad varchar(38),country varchar(20),mp decimal(5,2) default 0 ,sca decimal(5,2) default 0,passlive decimal(5,2) default 0,squadsanaccent VARCHAR)""")
        self.cur.execute("DELETE FROM goalshotcreation")

        self.cur.execute( """CREATE TABLE IF NOT EXISTS astats(pid integer default 0 PRIMARY KEY , player varchar(38),country varchar(20),position varchar(10),
    squad varchar(20),league varchar(25),age integer default 0, born integer default 0, mtplayed integer default 0, starts integer default 0,min integer default 0, playedfull decimal(5,2) default 0, 
    goals integer default 0, assist integer default 0, nonpen integer default 0,penaltiesmade integer default 0,penaltiesattempted  integer default 0,
    yellowcards integer default 0,redcards integer default 0,xgoals  decimal(5,2) default 0,xnonpeng decimal(5,2) default 0,
    xassist  decimal(5,2) default 0,xnonpencon  decimal(5,2) default 0,progc integer default 0,progp integer default 0,progr integer default 0)""")
        self.cur.execute("DELETE FROM astats")

        self.cur.execute(""" CREATE TABLE IF NOT EXISTS dstats( pid integer default 0 PRIMARY KEY,position varchar,mp decimal(5,2),tackles integer default 0, tacklewon integer default 0, tklondef integer default 0,tklonmid integer default 0,tklonatt integer default 0,
          duelwon integer default 0 ,duelatt integer default 0,  duelsucc decimal(5,2) default 0,duellost integer default 0,blocks integer default 0,shots_blocked integer default 0,pass_blocked integer default 0,interceptions integer default 0,tklint integer default 0,clearances integer default 0,errors integer default 0)""")
        self.cur.execute("DELETE FROM dstats")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS agkstats( pid integer default 0 ,player varchar(38),born integer default 0,mp decimal(5,2),goalsallowed integer default 0, pkgallowed integer default 0, fkgallowed integer default 0,ckgallowed integer default 0,ogagainst integer default 0,
    psxg  decimal(5,2) default 0,psxg_sot decimal(5,2) default 0,psxgpn varchar(8),gklaunchper  decimal(5,2) default 0,crossstpper decimal(5,2) default 0,opa  decimal(5,2) default 0,avgdistswp decimal(5,2) default 0)""")
        self.cur.execute("DELETE FROM agkstats")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS gkstats( pid integer default 0 ,player varchar(38),born integer default 0,saves integer default 0, savesper  decimal(5,2) default 0,pksv integer default 0)""")
        self.cur.execute("DELETE FROM gkstats")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS shooting( pid integer default 0 PRIMARY KEY, sotper  decimal(5,2) default 0,shperm  decimal(5,2) default 0,sotperm  decimal(5,2) default 0,shotconv decimal(5,2) default 0,npgnpxg  decimal(5,2) default 0)""")
        self.cur.execute("DELETE FROM shooting")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS gca( pid integer default 0 PRIMARY KEY ,mp decimal(5,2),sca integer default 0,scapasslive integer default 0,scapassdead integer default 0)""")
        self.cur.execute("DELETE FROM gca")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS passing( pid integer default 0 PRIMARY KEY,position varchar, mp decimal(5,2),att integer default 0,compper decimal(5,2) default 0,spatt integer default 0,spcmp integer default 0, spcmpper  decimal(5,2) default 0,mpatt integer default 0,mpcmp integer default 0,mpcmpper  decimal(5,2) default 0,lpatt integer default 0,lpcmp integer default 0,lpcmpper  decimal(5,2) default 0,xag decimal(5,2) default 0,xa decimal(5,2) default 0,axag decimal(5,2) default 0,kp integer default 0,final3rdpasses integer default 0,ppa integer default 0,crspa integer default 0)""")
        self.cur.execute("DELETE FROM passing")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS possession( pid integer default 0 PRIMARY KEY,position varchar,mp decimal(5,2),tdefpen integer default 0,tdef integer default 0,tmid integer default 0,tatt integer default 0,tattpen integer default 0,tlive integer default 0,dribatt integer default 0,dribsucc integer default 0,dribsuccper decimal(5,2) default 0,dribtkld integer default 0,dribtkldper decimal(5,2) default 0,carries integer default 0,carriestotdist integer default 0,carriesprgdist integer default 0,attcarries integer default 0,cpa integer default 0,miscon integer default 0,dispos integer default 0)""")
        self.cur.execute("DELETE FROM possession")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS passtypes( pid integer default 0 PRIMARY KEY,attemp integer default 0,live integer default 0,dead integer default 0,fk integer default 0,tb integer default 0,sw integer default 0,crs integer default 0 ,ti integer default 0 )""")
        self.cur.execute("DELETE FROM passtypes")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS misstats( pid integer default 0 PRIMARY KEY, recov integer default 0,aerialswon integer default 0,aerialswonper  decimal(5,2) default 0)""")
        self.cur.execute("DELETE FROM misstats")
        self.con.commit()


    def process_item(self, item, spider):

      if spider.name==FbrefSpider.name:
        rows= item['row'].split("!")
        if not rows[0].isalpha() and rows[0]!='':
            self.cur.execute('insert into lstanding values( :1, :2, :3, :4,:5,:6,:7, :8, :9, :10, :11, :12,:13,:14,:15,:16,:17,:18)',
                (rows[1], rows[2], rows[3],rows[4],rows[5], rows[6], rows[7],rows[8],rows[9],rows[10],rows[11],rows[12],rows[13],rows[14],rows[15],rows[16],rows[18],rows[19]))
            self.con.commit()

      elif spider.name==FbrefSCASpider.name:
        rows= item['row'].split("!")
        if not rows[0].isalpha() and rows[0]!='' :
            self.cur.execute('insert into goalshotcreation values( :1, :2, :3, :4,:5 ,:6)',
                (rows[1], rows[2], rows[4],rows[5],rows[7],"NULL"))
            self.con.commit()

      elif  spider.name==FbrefAGKSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute( 'insert into agkstats values( :1, :2, :3, :4,:5,:6,:7, :8, :9,:10,:11,:12,:13,:14,:15,:16)', (rows[0], rows[1], rows[7],rows[8], rows[9], rows[10], rows[11], rows[12], rows[13], rows[14], rows[15], rows[16],rows[26], rows[30], rows[32], rows[33]))
              self.con.commit()
      elif  spider.name==FbrefGKSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute( 'insert into gkstats values( :1, :2, :3, :4,:5,:6)', (rows[0], rows[1], rows[7], rows[15], rows[16], rows[24]))
              self.con.commit()

      elif  spider.name==FbrefDEFSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into dstats values( :1, :2, :3, :4,:5,:6,:7, :8, :9, :10, :11, :12,:13,:14,:15,:16,:17,:18,:19)',(rows[0],rows[3], rows[8],rows[9], rows[10], rows[11], rows[12], rows[13], rows[14],rows[15],rows[16],rows[17], rows[18], rows[19], rows[20], rows[21],
              rows[22],rows[23], rows[24]))
              self.con.commit()


      elif  spider.name==FbrefSTDSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into astats values( :1, :2, :3, :4,:5,:6,:7, :8, :9, :10, :11, :12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26)', (
              rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9], rows[10],
              rows[11],rows[12], rows[13], rows[15], rows[16], rows[17], rows[18], rows[19], rows[20], rows[21], rows[22], rows[23], rows[24], rows[25], rows[26]))
              self.con.commit()
      elif  spider.name==FbrefSHTSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into shooting values( :1, :2, :3,:4,:5,:6)',(rows[0], rows[12],rows[13],rows[14], rows[15],rows[25]))
              self.con.commit()
      elif  spider.name==FbrefGCASpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into gca values( :1, :2,:3,:4,:5)',(rows[0], rows[8],rows[9],rows[11],rows[12]))
              self.con.commit()


      elif  spider.name==FbrefPASSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into passing values( :1, :2, :3, :4,:5,:6,:7, :8, :9, :10, :11, :12,:13,:14,:15,:16,:17,:18,:19,:20,:21)',(rows[0],rows[3],rows[8],  rows[10], rows[11], rows[14],rows[15],rows[16],rows[17],rows[18],rows[19],rows[20],rows[21],rows[22], rows[24], rows[25],rows[26],
            rows[27],rows[28],rows[29],rows[30]))
              self.con.commit()
      elif  spider.name==FbrefPOSSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into possession values( :1, :2, :3, :4,:5,:6,:7, :8, :9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21)',(rows[0],rows[3],rows[8], rows[10], rows[11], rows[12], rows[13], rows[14], rows[15], rows[16], rows[17], rows[18], rows[19], rows[20], rows[21], rows[22], rows[23], rows[25], rows[26], rows[27],
              rows[28]))
              self.con.commit()
      elif  spider.name==FbrefPSTSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into passtypes values( :1, :2, :3, :4,:5,:6,:7,:8,:9)',(rows[0],rows[9],rows[10], rows[11], rows[12], rows[13], rows[14], rows[15],rows[16]))
              self.con.commit()
      elif  spider.name==FbrefMISSpider.name:
          rows = item['row'].split("!")
          if not rows[0].isalpha() and rows[0]!='':
              self.cur.execute('insert into misstats values( :1, :2, :3, :4)',(rows[0],  rows[21],rows[22], rows[24]))
              self.con.commit()

      return item