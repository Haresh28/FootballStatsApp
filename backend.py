
import sqlite3
import time
from scrapy.settings import Settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapyfbref import  settings as fbrefsettings
from scrapytiles import  settings as trfmktsettings
from scrapymarkstats import  settings as mssettings
from scrapymarkstatsplayers import  settings as mspsettings
from scrapy.utils.project import get_project_settings
from scrapymarkstats.spiders.markstats import MSSpider
from scrapymarkstatsplayers11.spiders.markstats import MSPSpider
from scrapyfbref.spiders.fbref import FbrefSpider,FbrefSCASpider,FbrefGKSpider,FbrefDEFSpider,FbrefSTDSpider,FbrefAGKSpider,FbrefGCASpider,FbrefMISSpider,FbrefPOSSpider,FbrefPSTSpider,FbrefPASSpider,FbrefSHTSpider


from scrapytiles.spiders.transferspider import TransferENGSpider,TransferESPSpider,TransferITASpider,TransferGERSpider,TransferFRASpider
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
from PyQt5.QtCore import pyqtSlot
import pyqtdashboard
import sys

#original
class UI(QMainWindow):
    def opendashboard(self):
        self.window=QtWidgets.QMainWindow()
        self.dashwindow=pyqtdashboard.ClubDashboard()
        self.dashwindow.setUp(self.window,[self.pl,self.laliga,self.bundesliga,self.seriea,self.ligue1])
        self.dashwindow.show()
    def __init__(self):
        super(UI,self).__init__()
    #somewhere in constructor:
        uic.loadUi("main_window.ui", self)
        self.password='/thiyagarajan'
    #initializing
        self.table=self.findChild(QTableWidget,"tableWidget")
        self.comboleague=self.findChild(QComboBox,"comboBox")
        self.comboclub=self.findChild(QComboBox,"comboBox_2")
        #self.progressbar=self.findChild(QProgressBar,"progressBar")
        self.tab=self.findChild(QTabWidget,"tabWidget")
        self.valuesetter()
    #setting values
        self.comboleague.width = 161
        self.leaguenames= ["Premier League", "La Liga", "Bundesliga", "Ligue 1", "Serie A"]

        self.comboleague.addItems(self.leaguenames)
        self.actionClub_Analysis.triggered.connect(lambda :self.opendashboard())
        #self.proxymodel=QSortFil
        #self.table.cellClicked(sort)
        self.comboleague.activated.connect(self.teamNames)
        self.comboclub.activated.connect(self.setup)
        #self.comboclub.setEnabled(False)


        self.show()
    def valuesetter(self):
        if not os.path.isfile("fbref.db"):
            self.master_scrapper()

        con=sqlite3.connect("fbref.db")
        cur =con.cursor()
        cur.execute("select squad from lstanding  order by country ")
        records=cur.fetchall()
        self.pl =[x[0] for x in records[18:38]]
        self.laliga = [x[0] for x in records[38:58]]
        self.bundesliga =[x[0] for x in records[0:18]]
        self.seriea = [x[0] for x in records[78:98]]
        self.ligue1 = [x[0] for x in records[58:78]]
        print(self.pl)
        cur.close()

    def teamNames(self):
        self.comboclub.clear()
        if (self.comboleague.currentText() == "Premier League"):
            self.comboclub.addItems( self.pl)
            self.comboclub.setCurrentText("Pick a club")
            #league = tables[0]
        elif (self.comboleague.currentText() == "La Liga"):
            self.comboclub.addItems(self.laliga)
            self.comboclub.setCurrentText("Pick a club")
            #league = tables[1]
        elif (self.comboleague.currentText() == "Bundesliga"):
            self.comboclub.addItems(self.bundesliga)
            self.comboclub.setCurrentText("Pick a club")
            #league = tables[2]
        elif (self.comboleague.currentText() == "Serie A"):
            self.comboclub.addItems(self.seriea)
            self.comboclub.setCurrentText("Pick a club")
            #league = tables[3]
        else:
            self.comboclub.addItems(self.ligue1)
            self.comboclub.setCurrentText("Pick a club")
            #league = tables[4]

    def update_gkstats(self):
        con = sqlite3.connect('fbref.db')
        cursor = con.cursor()
        cursor.execute("""UPDATE gkstats
            SET pid = (SELECT a.pid from astats AS a  where a.player=gkstats.player AND a.born=gkstats.born AND a.position="GK")
             """)
        # for zone domination
        sqdpossesionlink = 'https://fbref.com/en/comps/Big5/possession/squads/Big-5-European-Leagues-Stats'
        temp = pd.read_html(sqdpossesionlink, match='Squad Possession', flavor='bs4')

        for i in range(2):
            # to get rid of heirarchial cols
            temp[i].columns = temp[i].columns.to_flat_index()
            temp[i].columns = [x[1] for x in temp[i].columns]

            # removing null values
            temp[i].dropna(subset=['Squad', 'Comp'], inplace=True)
            temp[i] = temp[i].drop(temp[i][temp[i]['Squad'] == 'Squad'].index)
            temp[i].fillna(0, inplace=True)

        print("succ")

        sqlcommand4 = """create table if not exists zonedomination( squad varchar(20),defpen real, def3rd real, mid3rd real,att3rd real,attpen real,totaltouches real,
                vsdefpen real,vsdef3rd real, vsmid3rd real,vsatt3rd real,vsattpen real,vstotaltouches real
                                        )"""
        #print(type(temp[0].iloc[i, 1]),temp[0].iloc[i, 1].dtype)
        cursor.execute(sqlcommand4)
        cursor.execute("delete from zonedomination")
        for i in range(len(temp[0])):
            insertcmd = 'insert into zonedomination values( :1, :2, :3, :4,:5,:6,:7, :8, :9,:10,:11,:12,:13)'
            cursor.execute(insertcmd, (
            temp[0].iloc[i, 1], int(temp[0].iloc[i, 7]), int(temp[0].iloc[i, 8]), int(temp[0].iloc[i, 9]), int(temp[0].iloc[i, 10]),
            int(temp[0].iloc[i, 11]), int(temp[0].iloc[i, 6]), int(temp[1].iloc[i, 7]), int(temp[1].iloc[i, 8]), int(temp[1].iloc[i, 9]),
            int(temp[1].iloc[i, 10]), int(temp[1].iloc[i, 11]), int(temp[1].iloc[i, 6])))

        con.commit()
        cursor.close()

    def processing_raw(self):
        con = sqlite3.connect("fbref.db")
        cur = con.cursor()
        cur.execute("""create table if not exists transferstats( leaguernk integer ,squad varchar(20)
        ,league varchar(20),attage decimal(5,2),attval decimal(5,2),attavgval decimal(5,2),defage decimal(5,2),defval decimal(5,2)
        ,defavgval decimal(5,2),gkage decimal(5,2),gkval decimal(5,2),gkavgval decimal(5,2),
        totage decimal(5,2),totval decimal(5,2),totavgval decimal(5,2))

        """)
        cur.execute("delete from transferstats")
        cur.execute("select * from rawtransferstats order by league ,leaguernk ,position")
        records = cur.fetchall()
        cur.execute("select leaguernk,squad,country from lstanding order by country ,leaguernk ")
        squadvalues = cur.fetchall()

        for i in range(0, len(records), 4):
            cur.execute("insert into transferstats values( :1, :2, :3, :4,:5,:6,:7, :8, :9, :10, :11, :12,:13,:14,:15)",
                        (squadvalues[int(i / 4)][0], squadvalues[int(i / 4)][1], squadvalues[int(i / 4)][2],
                         records[i][3], records[i][4], records[i][5],
                         records[i + 1][3], records[i + 1][4], records[i + 1][5], records[i + 2][3], records[i + 2][4],
                         records[i + 2][5],
                         records[i + 3][3], records[i + 3][4], records[i + 3][5]))
            con.commit()

        cur.execute("create table if not EXISTS squadkey (fbrefsquad varchar ,markstatssquad varchar)");
        cur.execute("DELETE from goalshotcreation where squad like ' vs %'");
        cur.execute("DELETE  from squadkey");
        cur.execute("""update goalshotcreation set squadsanaccent=replace(replace(replace(replace(replace(replace(replace(squad,'ö','o'),'é','e'),'í','i'),'á','a'),"'",'.'),'Manchester','Man'),'-','');""");
        print("ssf")
        cur.execute("insert into squadkey SELECT s.squad as ss, m.squad as ms from markstats as m,goalshotcreation as s where trim(s.country)=trim(m.country)  and  m.squad like '%'|| s.squadsanaccent ||'%' or s.squadsanaccent like '%'|| m.squad ||'%' ");
        cur.execute("insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey) and (substr(trim(m.squad),1,instr(trim(m.squad),' ')-1)=substr(trim(s.squadsanaccent),1,instr(trim(s.squadsanaccent),' ')-1) or substr(trim(m.squad),instr(trim(m.squad),' ')+1)=substr(trim(s.squadsanaccent),instr(trim(s.squadsanaccent),' ')+1))");
        cur.execute("insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey)");

        cur.execute("create table if not EXISTS dummy (fbrefplayer varchar,playersanaccent varchar,country varchar)")
        cur.execute("insert into dummy select player,player,league from astats")
        cur.execute("create table if not EXISTS playerkey (fbrefplayer varchar ,markstatsplayer varchar)");

        cur.execute("DELETE  from playerkey")
        cur.execute(
            """update dummy set playersanaccent=replace(replace(replace(replace(replace(replace(replace(playersanaccent,'ö','o'),'é','e'),'í','i'),'á','a'),'ñ','n'),'ć','c'),'-','')""")
        cur.execute("""update markstatsplayers set playersanaccent=replace(replace(replace(replace(replace(replace(replace(playersanaccent,'ö','o'),'é','e'),'í','i'),'á','a'),'ñ','n'),'ć','c'),'-','')""")
        print("ssf")
        """
        used on markstatsplayers   ----
        show collation like "utf8_unicode_520_ci"
utf8_unicode_520_ci
        
        SELECT s.fbrefplayer as ss, m.player as ms from markstatsplayers as m,dummy as s where trim(s.country)=trim(m.country)  and  m.player like  s.playersanaccent or   s.playersanaccent like m.player """
        cur.execute(
            "insert into squadkey SELECT s.squad as ss, m.squad as ms from markstats as m,goalshotcreation as s where trim(s.country)=trim(m.country)  and  m.squad like '%'|| s.squadsanaccent ||'%' or s.squadsanaccent like '%'|| m.squad ||'%' ");
        cur.execute(
            "insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey) and (substr(trim(m.squad),1,instr(trim(m.squad),' ')-1)=substr(trim(s.squadsanaccent),1,instr(trim(s.squadsanaccent),' ')-1) or substr(trim(m.squad),instr(trim(m.squad),' ')+1)=substr(trim(s.squadsanaccent),instr(trim(s.squadsanaccent),' ')+1))");

        cur.execute(
            "insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey) and (substr(trim(m.squad),1,instr(trim(m.squad),' ')-1)=substr(trim(s.squadsanaccent),1,instr(trim(s.squadsanaccent),' ')-1) or substr(trim(m.squad),instr(trim(m.squad),' ')+1)=substr(trim(s.squadsanaccent),instr(trim(s.squadsanaccent),' ')+1))");

        cur.execute(
            "insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey)");

        con.commit()
        cur.close()



    def master_scrapper(self):

        configure_logging()
        crawler_settings = Settings()
        crawler_settings.setmodule(trfmktsettings)
        runner = CrawlerRunner(settings=crawler_settings)
        crawler_settings2 = Settings()
        crawler_settings2.setmodule(fbrefsettings)
        runner2 = CrawlerRunner(settings=crawler_settings2)
        crawler_settings3 = Settings()
        crawler_settings3.setmodule(mssettings)
        runner3 = CrawlerRunner(settings=crawler_settings3)
        crawler_settings4 = Settings()
        crawler_settings4.setmodule(mspsettings)
        runner4 = CrawlerRunner(settings=crawler_settings4)
        @defer.inlineCallbacks
        def crawl():

            yield runner2.crawl(FbrefSTDSpider)
            yield runner2.crawl(FbrefSCASpider)
            yield runner2.crawl(FbrefDEFSpider)
            yield runner2.crawl(FbrefSpider)
            yield runner2.crawl(FbrefGKSpider)
            yield runner2.crawl(FbrefPASSpider)
            yield runner2.crawl(FbrefPSTSpider)
            yield runner2.crawl(FbrefPOSSpider)
            yield runner2.crawl(FbrefSHTSpider)
            yield runner2.crawl(FbrefAGKSpider)
            yield runner2.crawl(FbrefMISSpider)
            yield runner2.crawl(FbrefGCASpider)


            yield runner.crawl(TransferESPSpider)
            yield runner.crawl(TransferFRASpider)
            yield runner.crawl(TransferGERSpider)
            yield runner.crawl(TransferITASpider)
            yield runner.crawl(TransferENGSpider)

            yield runner3.crawl(MSSpider)
            yield runner4.crawl(MSPSpider)
            reactor.stop()

        crawl()
        reactor.run()
        time.sleep(3)
        self.update_gkstats()
        self.processing_raw()

    # setting up table based on league and team 3rd combobox
    def setup(self):
        print("ok")
        self.table.clearContents()

        self.update_gkstats()#need to calll from a button
        con = sqlite3.connect('fbref.db')
        c = con.cursor()
        print("ok")

        cmd = "select * from  astats where league like :1 and squad = :2  "

        c.execute(cmd, ('%'+self.comboleague.currentText(), self.comboclub.currentText()[1:]))
        records = c.fetchall()
        print(len(records))
        c.execute("SELECT name FROM PRAGMA_TABLE_INFO('astats')")
        column = c.fetchall()

        columns = [x[0] for x in column]

        print("ok before inster")
        self.table.horizontalHeader().setVisible(True)
        self.table.verticalHeader().setVisible(True)
        self.table.setColumnCount(len(columns))

        self.table.setRowCount(len(records))
        self.table.setHorizontalHeaderLabels(columns)


        self.table.setViewportMargins(QMargins(178,31,0,0))
        print(self.table.verticalScrollMode(),"margins",self.table.viewportMargins().left(),self.table.viewportMargins().top(),self.table.viewportMargins().right(),self.table.viewportMargins().bottom())

        self.table.setColumnWidth(0, 150)
        for j,r in enumerate(records):
            for i,item in enumerate(r):
                self.table.setItem(j, i, QTableWidgetItem(str(item) ))




        c.close()


if __name__ =="__main__":
    app=QApplication(sys.argv)
    wnd=UI()
    app.exec_()




